<?php

declare(strict_types=1);

namespace Revaly\Sdk;

use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\RequestOptions;
use GuzzleHttp\Utils as GuzzleUtils;
use Psr\Log\LoggerInterface;
use Psr\Log\NullLogger;
use Revaly\Sdk\Core\Api\NotifyApi;
use Revaly\Sdk\Core\Api\PaymentMethodsApi;
use Revaly\Sdk\Core\Api\PaymentsApi;
use Revaly\Sdk\Core\Api\TransactionsApi;
use Revaly\Sdk\Core\ApiException;
use Revaly\Sdk\Core\Configuration;
use Revaly\Sdk\Core\Model\AuthorizeRequest;
use Revaly\Sdk\Core\Model\CaptureRequest;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Core\Model\RefundCancelRequest;
use Revaly\Sdk\Core\Model\RefundRequest;
use Revaly\Sdk\Core\Model\TransactionResponse;
use Revaly\Sdk\Core\Model\VoidRequest;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Errors\FailureClassifier;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\RapCoreException;
use Revaly\Sdk\Logging\RapScrubber;
use Revaly\Sdk\Logging\RapWireTrace;
use Revaly\Sdk\Reconcile\RapReconciler;
use Revaly\Sdk\Reconcile\RapReconcileVerdict;
use Revaly\Sdk\Reconcile\ReconcilePolicy;
use Revaly\Sdk\Transport\DispatchCounter;
use Revaly\Sdk\Transport\RapHeaders;
use Revaly\Sdk\Transport\RapTransport;
use Revaly\Sdk\Transport\RapUserAgent;

/**
 * The RAP PHP SDK client (runtime-tdd §§1-2): one client object per configuration —
 * create it once and reuse it (no global singletons).
 *
 * Payment operations return the core's {@see TransactionResponse} on success and throw
 * exactly one of the three typed failure classes on failure (docs/failover-contract.md §2):
 *
 * - {@see \Revaly\Sdk\Errors\PermanentRejectionException} — fix or decline; never fail over.
 * - {@see \Revaly\Sdk\Errors\TransientFailureException} — definitively not processed;
 *   safe to fail over immediately.
 * - {@see \Revaly\Sdk\Errors\OutcomeUnknownException} — may have been processed;
 *   {@see reconcile()} before acting.
 *
 * The full generated V2 surface stays available through {@see payments()},
 * {@see transactions()}, {@see paymentMethods()} and {@see notifyApi()} — one
 * dependency, one package to import.
 */
final class RapClient
{
    private readonly string $apiVersion;
    private readonly GuzzleClient $guzzle;
    private readonly LoggerInterface $logger;
    private readonly ?\Closure $wireTraceHook;
    private readonly bool $emitPayloadTraces;
    private readonly DispatchCounter $dispatches;
    private readonly PaymentsApi $payments;
    private readonly TransactionsApi $transactions;
    private readonly PaymentMethodsApi $paymentMethods;
    private readonly NotifyApi $notify;
    private readonly RapReconciler $reconciler;

    /**
     * The overall-deadline default applied when the parameter is omitted: 75 seconds,
     * ratified from production latency telemetry (ADR-SDK-027). Pass an explicit
     * `overallDeadline: null` to disable the SDK deadline entirely.
     */
    public const DEFAULT_OVERALL_DEADLINE_SECONDS = 75.0;

    /**
     * @param string $apiKey the merchant API key (required). Sent as
     *        `Authorization: ApiKey <key>` on every request; never persisted, never
     *        logged, never present in exception messages (ADR-SDK-020).
     * @param string $baseUrl the API base URL. Defaults to `https://api.revaly.co` —
     *        sandbox and live share this URL; the environment is selected by your API
     *        key's scope, not the URL. Override only for internal/pre-release targets.
     * @param string $apiVersion the API contract version, pinned via `X-Api-Version` on
     *        every request. Default "2.1"; "2.0" is selectable. Behavioural difference
     *        on "2.0": the `ErrorResponse.code` field is not part of the 2.0 documented
     *        contract, so the fast-failover class narrows to client-provable never-sent
     *        failures only — a 503 with `code: not_processed` classifies as
     *        OutcomeUnknown (reconcile) instead of TransientFailure (immediate
     *        failover). Pin 2.1 unless you have a frozen 2.0 integration.
     * @param float|null $connectTimeout TCP/TLS connection-establishment timeout in
     *        seconds. Default: none set by this SDK — the transport waits per its own
     *        default. A client-side connect default cannot be derived from server-side
     *        telemetry; it awaits the OQ-11 edge verification (ADR-SDK-027) and this
     *        SDK deliberately does not invent one. Note: curl reports a connect-phase
     *        timeout and an after-send timeout with the same error, so BOTH classify
     *        OutcomeUnknown (never TransientFailure).
     * @param float|null $overallDeadline overall per-request deadline in seconds.
     *        Expiry after the request was sent classifies as OutcomeUnknown (reconcile
     *        before acting) — never TransientFailure. Default:
     *        {@see self::DEFAULT_OVERALL_DEADLINE_SECONDS} (75 seconds, ratified from
     *        production latency telemetry — ADR-SDK-027; it clears every observed
     *        gateway tail cluster and clips ≲0.007% of charges). Pass an explicit
     *        null to disable the SDK deadline (the transport then waits indefinitely).
     * @param LoggerInterface|null $logger PSR-3 logger. Default output is VALUES-FREE:
     *        operation, status, class, and correlation id only; debug level carries
     *        allowlist-scrubbed payloads (ADR-SDK-020).
     * @param callable|null $wireTraceHook optional request/response observer for
     *        Enablement escalations: `function (RapWireTrace $trace): void`. Receives
     *        payloads already scrubbed by the runtime's central allowlist scrubber —
     *        never raw material. Observer exceptions are swallowed.
     * @param callable|null $transport replacement wire transport (a Guzzle handler).
     *        Intended for the mock transport ({@see \Revaly\Sdk\Testing\RapMockTransport})
     *        in merchant tests; null uses the real HTTP transport.
     * @param string|null $userAgentSuffix optional merchant product token APPENDED
     *        after the SDK's User-Agent token (ADR-SDK-005: the SDK prefix stays first
     *        and intact; it can never be replaced or suppressed).
     */
    public function __construct(
        string $apiKey,
        string $baseUrl = 'https://api.revaly.co',
        string $apiVersion = '2.1',
        ?float $connectTimeout = null,
        ?float $overallDeadline = self::DEFAULT_OVERALL_DEADLINE_SECONDS,
        ?LoggerInterface $logger = null,
        ?callable $wireTraceHook = null,
        ?callable $transport = null,
        ?string $userAgentSuffix = null,
    ) {
        if (trim($apiKey) === '') {
            throw new \InvalidArgumentException('apiKey is required');
        }
        if (trim($baseUrl) === '') {
            throw new \InvalidArgumentException('baseUrl is required');
        }
        if (trim($apiVersion) === '') {
            throw new \InvalidArgumentException('apiVersion is required');
        }
        if ($connectTimeout !== null && $connectTimeout <= 0) {
            throw new \InvalidArgumentException('connectTimeout must be positive when set');
        }
        if ($overallDeadline !== null && $overallDeadline <= 0) {
            throw new \InvalidArgumentException('overallDeadline must be positive when set');
        }

        $baseUrl = rtrim($baseUrl, '/');
        $this->apiVersion = $apiVersion;
        $this->logger = $logger ?? new NullLogger();
        $this->wireTraceHook = $wireTraceHook === null ? null : \Closure::fromCallable($wireTraceHook);
        $this->emitPayloadTraces = $this->wireTraceHook !== null || !($this->logger instanceof NullLogger);
        $this->dispatches = new DispatchCounter();

        $userAgent = RapUserAgent::value($userAgentSuffix);

        // One shared Guzzle client for the whole surface (core apis + reconciler). The
        // runtime middlewares sit closest to the wire, so the mock transport sees
        // exactly what the network would (DX contract §d).
        $stack = HandlerStack::create($transport ?? GuzzleUtils::chooseHandler());
        $stack->push(
            RapTransport::headerMiddleware($apiKey, $apiVersion, $userAgent, $this->dispatches),
            'rap_headers',
        );
        $stack->push(RapTransport::classificationMiddleware(), 'rap_classify');

        $this->guzzle = new GuzzleClient([
            'handler' => $stack,
            // A followed redirect could silently resubmit a payment (307/308 re-send
            // the body) — never follow; a 3xx classifies OutcomeUnknown instead.
            RequestOptions::ALLOW_REDIRECTS => false,
            RequestOptions::HTTP_ERRORS => true,
            RequestOptions::TIMEOUT => $overallDeadline ?? 0,
            RequestOptions::CONNECT_TIMEOUT => $connectTimeout ?? 0,
        ]);

        // The core Configuration deliberately never receives the API key — the header
        // middleware is the single injection point (ADR-SDK-020), and the core's
        // placeholder User-Agent is overwritten there too (ADR-SDK-005).
        $coreConfig = new Configuration();
        $coreConfig->setHost($baseUrl);
        $coreConfig->setUserAgent($userAgent);

        $this->payments = new PaymentsApi($this->guzzle, $coreConfig);
        $this->transactions = new TransactionsApi($this->guzzle, $coreConfig);
        $this->paymentMethods = new PaymentMethodsApi($this->guzzle, $coreConfig);
        $this->notify = new NotifyApi($this->guzzle, $coreConfig);
        $this->reconciler = new RapReconciler(
            $this->guzzle,
            $baseUrl,
            $apiVersion,
            $this->logger,
            $this->wireTraceHook,
        );
    }

    /** Charges a payment (`POST /payments`). */
    public function charge(PaymentRequest $request): TransactionResponse
    {
        return $this->execute(
            'charge',
            'POST',
            '/payments',
            $request,
            fn (): array => $this->payments->chargePaymentWithHttpInfo($request, null),
        );
    }

    /** Authorizes a payment for later capture (`POST /payments/authorize`). */
    public function authorize(AuthorizeRequest $request): TransactionResponse
    {
        return $this->execute(
            'authorize',
            'POST',
            '/payments/authorize',
            $request,
            fn (): array => $this->payments->authorizePaymentWithHttpInfo($request, null),
        );
    }

    /** Captures a previously authorized payment. */
    public function capture(string $transactionId, CaptureRequest $request): TransactionResponse
    {
        return $this->execute(
            'capture',
            'POST',
            '/payments/capture/{transactionId}',
            $request,
            fn (): array => $this->payments->capturePaymentWithHttpInfo($transactionId, $request, null),
        );
    }

    /** Voids a previously authorized payment. */
    public function voidPayment(string $transactionId, VoidRequest $request): TransactionResponse
    {
        return $this->execute(
            'void',
            'POST',
            '/payments/void/{transactionId}',
            $request,
            fn (): array => $this->payments->voidPaymentWithHttpInfo($transactionId, $request, null),
        );
    }

    /** Refunds a settled payment. */
    public function refund(string $transactionId, RefundRequest $request): TransactionResponse
    {
        return $this->execute(
            'refund',
            'POST',
            '/payments/refund/{transactionId}',
            $request,
            fn (): array => $this->payments->refundPaymentWithHttpInfo($transactionId, $request, null),
        );
    }

    /** Cancels a refund by merchant transaction id. */
    public function refundCancel(string $merchantTransactionId, RefundCancelRequest $request): TransactionResponse
    {
        return $this->execute(
            'refundCancel',
            'POST',
            '/payments/refund-cancel/merchant/{merchantTransactionId}',
            $request,
            fn (): array => $this->payments->refundCancelPaymentByMerchantTransactionIdWithHttpInfo(
                $merchantTransactionId,
                $request,
                null,
            ),
        );
    }

    /**
     * The OutcomeUnknown reconciliation procedure (failover-contract §3): polls the
     * merchant-transaction lookup within the caller-bounded {@see ReconcilePolicy} and
     * returns {@see \Revaly\Sdk\Reconcile\Found} or
     * {@see \Revaly\Sdk\Reconcile\NotFoundYet}. ALWAYS branch with a default — verdicts
     * are open for extension (SafeToFailover arrives with platform P-2 as a minor
     * release).
     */
    public function reconcile(string $merchantTransactionId, ReconcilePolicy $policy): RapReconcileVerdict
    {
        return $this->reconciler->reconcile($merchantTransactionId, $policy);
    }

    /** The generated payments api, sharing this client's transport and headers. */
    public function payments(): PaymentsApi
    {
        return $this->payments;
    }

    /** The generated transactions api, sharing this client's transport and headers. */
    public function transactions(): TransactionsApi
    {
        return $this->transactions;
    }

    /** The generated payment-methods api, sharing this client's transport and headers. */
    public function paymentMethods(): PaymentMethodsApi
    {
        return $this->paymentMethods;
    }

    /** The generated notify api, sharing this client's transport and headers. */
    public function notifyApi(): NotifyApi
    {
        return $this->notify;
    }

    /**
     * @param \Closure(): array{0: mixed, 1: int, 2: array<string, array<string>>} $call
     */
    private function execute(
        string $operation,
        string $method,
        string $path,
        object $requestModel,
        \Closure $call,
    ): TransactionResponse {
        $dispatchesBefore = $this->dispatches->count;

        try {
            [$data, $statusCode, $headers] = $call();
        } catch (RapCoreException $classified) {
            // Transport-level failure, already typed by the classification middleware.
            $this->logFailure($operation, $classified);
            $this->trace($operation, $method, $path, $classified->getStatusCode(), $classified->getCorrelationId(), $requestModel, null);

            throw $classified;
        } catch (ApiException $e) {
            $classified = $this->translate($e);
            $this->logFailure($operation, $classified);
            $this->trace($operation, $method, $path, $classified->getStatusCode(), $classified->getCorrelationId(), $requestModel, null);

            throw $classified;
        } catch (\Throwable $failure) {
            if ($this->dispatches->count === $dispatchesBefore) {
                // The request never reached the transport (core request validation
                // rejected it) — a caller error, not a payment outcome.
                throw $failure;
            }
            // The request WAS dispatched and a response arrived, but this SDK version
            // could not read it (e.g. the core's standalone-enum deserialize edge on a
            // server-newer-than-spec value — generator-bakeoff §A3). The outcome is
            // unknowable locally; reconcile resolves it from the raw record.
            $classified = new OutcomeUnknownException(
                'response received but unreadable by this SDK version; reconcile before acting',
                previous: $failure,
            );
            $this->logFailure($operation, $classified);
            $this->trace($operation, $method, $path, null, null, $requestModel, null);

            throw $classified;
        }

        $correlationId = self::correlationFrom($headers);
        $this->logger->info(
            'rap.request operation={operation} status={status} correlation={correlation}',
            ['operation' => $operation, 'status' => $statusCode, 'correlation' => $correlationId],
        );
        $this->trace($operation, $method, $path, $statusCode, $correlationId, $requestModel, $data);

        return $data;
    }

    private function translate(ApiException $e): RapCoreException
    {
        $statusCode = (int) $e->getCode();
        if ($statusCode === 0) {
            // No response and no typed middleware failure — a transport failure from a
            // path that carries no structured never-sent proof: the conservative branch.
            return FailureClassifier::classifyTransportRejection($e->getPrevious() ?? $e);
        }

        $rawBody = $e->getResponseBody();
        $rawBody = is_string($rawBody) ? $rawBody : null;

        return FailureClassifier::classifyResponse(
            $statusCode,
            $rawBody,
            $this->apiVersion,
            self::correlationFrom($e->getResponseHeaders()),
        );
    }

    private function logFailure(string $operation, RapCoreException $classified): void
    {
        $this->logger->warning(
            'rap.request failed operation={operation} class={class} status={status} code={code} correlation={correlation}',
            [
                'operation' => $operation,
                'class' => $classified->getFailureClass()->value,
                'status' => $classified->getStatusCode(),
                'code' => $classified->getErrorCode(),
                'correlation' => $classified->getCorrelationId(),
            ],
        );
    }

    private function trace(
        string $operation,
        string $method,
        string $path,
        ?int $status,
        ?string $correlationId,
        ?object $requestModel,
        ?object $responseModel,
    ): void {
        if (!$this->emitPayloadTraces) {
            return;
        }

        $scrubbedRequest = $this->scrubModel($requestModel);
        $scrubbedResponse = $this->scrubModel($responseModel);

        // Debug level carries allowlist-scrubbed payloads only (ADR-SDK-020).
        $this->logger->debug(
            'rap.request payload operation={operation} request={request} response={response}',
            ['operation' => $operation, 'request' => $scrubbedRequest, 'response' => $scrubbedResponse],
        );

        if ($this->wireTraceHook !== null) {
            try {
                ($this->wireTraceHook)(new RapWireTrace(
                    $operation,
                    $method,
                    $path,
                    $status,
                    $correlationId,
                    null,
                    $scrubbedRequest,
                    null,
                    $scrubbedResponse,
                ));
            } catch (\Throwable $hookFailure) {
                // Observer exceptions are swallowed (runtime-tdd §6).
                $this->logger->debug('rap.wiretrace hook threw; ignored', ['exception' => get_class($hookFailure)]);
            }
        }
    }

    private function scrubModel(?object $model): ?string
    {
        if ($model === null) {
            return null;
        }
        try {
            $json = json_encode(ObjectSerializer::sanitizeForSerialization($model));

            return RapScrubber::scrubJson($json === false ? null : $json);
        } catch (\Throwable $serializationFailure) {
            return RapScrubber::SCRUBBED;
        }
    }

    /**
     * @param array<mixed, array<string>>|null $headers
     */
    private static function correlationFrom(?array $headers): ?string
    {
        if ($headers === null) {
            return null;
        }
        foreach ($headers as $name => $values) {
            if (is_string($name) && strcasecmp($name, RapHeaders::CORRELATION_ID) === 0) {
                $values = (array) $values;
                $first = reset($values);

                return is_string($first) && $first !== '' ? $first : null;
            }
        }

        return null;
    }
}
