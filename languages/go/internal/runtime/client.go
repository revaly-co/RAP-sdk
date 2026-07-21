// The RAP client (runtime-tdd §§1–2): a thin, classified wrapper over the
// generated core. Every operation returns either the parsed result or exactly
// one of the three typed failure classes (errors.go); logs are values-free at
// every level (ADR-SDK-020).
package runtime

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"

	core "github.com/revaly-co/rap-sdk/languages/go/core"
)

// Client is the RAP client. Construct with NewClient; safe for concurrent use.
type Client struct {
	cfg        Config
	userAgent  string
	httpClient *http.Client
	coreClient *core.APIClient
	reconciler *reconciler
}

// NewClient validates the configuration and builds a client. The merchant API
// key is captured by the transport only — it is never placed on the core
// configuration, in a context value, in logs, or in error messages
// (ADR-SDK-020).
func NewClient(cfg Config) (*Client, error) {
	cfg, err := cfg.withDefaults()
	if err != nil {
		return nil, err
	}

	transport := cfg.Transport
	if transport == nil && cfg.HTTPClient != nil && cfg.HTTPClient.Transport != nil {
		transport = cfg.HTTPClient.Transport
	}
	if transport == nil {
		transport = newBaseTransport(cfg.ConnectTimeout)
	}

	userAgent := buildUserAgent()
	httpClient := &http.Client{
		Transport: &roundTripper{
			apiKey:     cfg.APIKey,
			apiVersion: cfg.APIVersion,
			userAgent:  userAgent,
			transport:  transport,
		},
		// Never follow redirects: a 307 re-POST would resubmit a payment
		// (probed); a 3xx comes back as-is and classifies OutcomeUnknown.
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	coreCfg := core.NewConfiguration()
	coreCfg.Servers = core.ServerConfigurations{{URL: cfg.BaseURL, Description: "configured base URL"}}
	coreCfg.HTTPClient = httpClient
	coreCfg.UserAgent = userAgent // cosmetic — the transport force-sets it regardless

	client := &Client{
		cfg:        cfg,
		userAgent:  userAgent,
		httpClient: httpClient,
		coreClient: core.NewAPIClient(coreCfg),
	}
	client.reconciler = &reconciler{
		httpClient: httpClient,
		baseURL:    cfg.BaseURL,
		apiVersion: cfg.APIVersion,
		logger:     cfg.Logger,
		trace:      cfg.WireTrace,
	}
	return client, nil
}

// Core exposes the full generated V2 surface (runtime-tdd §2) sharing this
// client's transport (auth, User-Agent, version pin, no redirects). Calls made
// directly on the core return core-shaped errors — the typed failure classes
// and the §2 classification exist only on the Client operations and Reconcile.
func (c *Client) Core() *core.APIClient { return c.coreClient }

// Charge processes a payment (POST /payments). merchantTransactionId is
// required on the request — it is the reconcile key (failover-contract §3).
func (c *Client) Charge(ctx context.Context, request *core.PaymentRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("Charge")
	}
	return executeOp(c, ctx, "charge", http.MethodPost, "/payments", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.ChargePayment(ctx).PaymentRequest(*request).Execute()
		})
}

// Authorize authorizes a payment (POST /payments/authorize).
func (c *Client) Authorize(ctx context.Context, request *core.AuthorizeRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("Authorize")
	}
	return executeOp(c, ctx, "authorize", http.MethodPost, "/payments/authorize", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.AuthorizePayment(ctx).AuthorizeRequest(*request).Execute()
		})
}

// Capture captures an authorized payment.
func (c *Client) Capture(ctx context.Context, transactionID string, request *core.CaptureRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("Capture")
	}
	return executeOp(c, ctx, "capture", http.MethodPost, "/payments/{transactionId}/capture", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.CapturePayment(ctx, transactionID).CaptureRequest(*request).Execute()
		})
}

// Void voids an authorized payment.
func (c *Client) Void(ctx context.Context, transactionID string, request *core.VoidRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("Void")
	}
	return executeOp(c, ctx, "void", http.MethodPost, "/payments/{transactionId}/void", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.VoidPayment(ctx, transactionID).VoidRequest(*request).Execute()
		})
}

// Refund refunds a captured payment.
func (c *Client) Refund(ctx context.Context, transactionID string, request *core.RefundRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("Refund")
	}
	return executeOp(c, ctx, "refund", http.MethodPost, "/payments/{transactionId}/refund", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.RefundPayment(ctx, transactionID).RefundRequest(*request).Execute()
		})
}

// RefundCancel cancels a refund by merchant transaction id.
func (c *Client) RefundCancel(ctx context.Context, merchantTransactionID string, request *core.RefundCancelRequest) (*core.TransactionResponse, error) {
	if request == nil {
		return nil, errNilRequest("RefundCancel")
	}
	return executeOp(c, ctx, "refund_cancel", http.MethodPost, "/payments/merchant/{merchantTransactionId}/refund-cancel", request,
		func(ctx context.Context) (*core.TransactionResponse, *http.Response, error) {
			return c.coreClient.PaymentsAPI.RefundCancelPaymentByMerchantTransactionId(ctx, merchantTransactionID).RefundCancelRequest(*request).Execute()
		})
}

// errNilRequest is the guard for a nil request struct — a plain programming
// error, deliberately NOT one of the three typed failure classes: no request
// was ever attempted, so there is no wire outcome to classify
// (failover-contract §2 untouched).
func errNilRequest(op string) error {
	return errors.New("revaly: " + op + ": request must not be nil")
}

// Reconcile runs the OutcomeUnknown reconciliation procedure
// (failover-contract §3) for the given merchantTransactionId under the
// caller-bounded policy. See reconcile.go for the verdict contract; the
// verdict set is OPEN — always dispatch with a default branch.
func (c *Client) Reconcile(ctx context.Context, merchantTransactionID string, policy ReconcilePolicy) (ReconcileVerdict, error) {
	return c.reconciler.reconcile(ctx, merchantTransactionID, policy)
}

// executeOp wraps one core Execute call: applies the configured overall
// deadline, classifies every failure into exactly one typed class, emits
// values-free logs, and feeds the scrubbed wire trace.
func executeOp[T any](
	c *Client,
	ctx context.Context,
	op string,
	method string,
	pathTemplate string,
	requestBody any,
	call func(context.Context) (T, *http.Response, error),
) (T, error) {
	var zero T
	if ctx == nil {
		ctx = context.Background()
	}
	if c.cfg.OverallDeadline > 0 {
		var cancel context.CancelFunc
		ctx, cancel = context.WithTimeout(ctx, c.cfg.OverallDeadline)
		defer cancel()
	}

	result, httpResp, err := call(ctx)

	status := 0
	correlationID := ""
	if httpResp != nil {
		status = httpResp.StatusCode
		correlationID = httpResp.Header.Get(CorrelationIDHeader)
	}

	if err == nil {
		c.cfg.Logger.Info("rap.op", "op", op, "status", status, "correlation", correlationID)
		if c.cfg.WireTrace != nil {
			emitTrace(c.cfg.Logger, c.cfg.WireTrace, WireTraceEvent{
				Operation:            op,
				Method:               method,
				Path:                 pathTemplate,
				Status:               status,
				CorrelationID:        correlationID,
				ScrubbedRequestBody:  scrubModel(requestBody),
				ScrubbedResponseBody: ScrubJSON(readBodyTail(httpResp)),
			})
		}
		return result, nil
	}

	typed := c.classifyExecuteError(err, httpResp)
	kind := "OutcomeUnknown"
	rawBody := ""
	switch failure := typed.(type) {
	case *PermanentRejection:
		kind, rawBody = failure.Kind, failure.RawBody
	case *TransientFailure:
		kind, rawBody = failure.Kind, failure.RawBody
	case *OutcomeUnknown:
		kind, rawBody = failure.Kind, failure.RawBody
	}
	c.cfg.Logger.Warn("rap.op failed", "op", op, "class", kind, "status", status, "correlation", correlationID)
	if c.cfg.WireTrace != nil {
		emitTrace(c.cfg.Logger, c.cfg.WireTrace, WireTraceEvent{
			Operation:            op,
			Method:               method,
			Path:                 pathTemplate,
			Status:               status,
			CorrelationID:        correlationID,
			ScrubbedRequestBody:  scrubModel(requestBody),
			ScrubbedResponseBody: ScrubJSON(rawBody),
		})
	}
	return zero, typed
}

// classifyExecuteError maps a core Execute failure to exactly one typed class.
func (c *Client) classifyExecuteError(err error, httpResp *http.Response) error {
	if httpResp == nil {
		// The request never produced a response: wire-level failure.
		return ClassifyTransportError(err)
	}

	status := httpResp.StatusCode
	correlationID := httpResp.Header.Get(CorrelationIDHeader)

	if status < 200 || status > 299 {
		return ClassifyResponse(status, errorBody(err, httpResp), correlationID, c.cfg.APIVersion)
	}

	// A 2xx that still errored: either the core could not read the body
	// (GenericOpenAPIError — e.g. a wrapper/decode failure) or the body read
	// itself failed mid-flight (raw transport error).
	var coreErr *core.GenericOpenAPIError
	if errors.As(err, &coreErr) {
		return &OutcomeUnknown{RapError{
			Kind:          "OutcomeUnknown",
			Status:        status,
			CorrelationID: correlationID,
			RawBody:       string(coreErr.Body()),
			message:       "OutcomeUnknown: 2xx response this SDK version could not read — reconcile before acting",
			cause:         err,
		}}
	}
	return ClassifyTransportError(err)
}

// errorBody recovers the raw response body for classification, preferring the
// core error's captured bytes, falling back to the (re-readable) response
// buffer the core leaves behind.
func errorBody(err error, httpResp *http.Response) string {
	var coreErr *core.GenericOpenAPIError
	if errors.As(err, &coreErr) && len(coreErr.Body()) > 0 {
		return string(coreErr.Body())
	}
	return readBodyTail(httpResp)
}

// readBodyTail drains the response buffer the core leaves re-readable
// (Execute replaces the body with a bytes buffer — probed). Returns "" when
// nothing is available.
func readBodyTail(httpResp *http.Response) string {
	if httpResp == nil || httpResp.Body == nil {
		return ""
	}
	data, err := io.ReadAll(httpResp.Body)
	if err != nil {
		return ""
	}
	return string(data)
}

// scrubModel renders any request model through the central scrubber.
func scrubModel(model any) string {
	if model == nil {
		return ""
	}
	data, err := json.Marshal(model)
	if err != nil {
		return Scrubbed
	}
	return ScrubJSON(string(data))
}
