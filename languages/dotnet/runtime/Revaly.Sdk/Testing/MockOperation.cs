using System.Net;
using System.Text;

namespace Revaly.Sdk.Testing;

/// <summary>
/// Scenario builder for one stubbed operation. Method names mirror the failover-contract
/// §2 taxonomy so merchant test code reads as the contract. Each call enqueues one
/// outcome; consecutive calls script consecutive outcomes (the last outcome repeats once
/// the script is exhausted), so suppression/escalation logic is testable:
/// <code>
/// mock.Reconcile(id).ReturnsNotFoundYet().ReturnsNotFoundYet().ReturnsApproved();
/// </code>
/// </summary>
public sealed class MockOperation
{
    private readonly Queue<Func<Exception?>> _preludes = new();
    private readonly Queue<Func<HttpResponseMessage>> _outcomes = new();
    private Func<HttpResponseMessage>? _last;
    private Func<Exception?>? _lastPrelude;

    internal MockOperation()
    {
    }

    internal HttpResponseMessage Next()
    {
        Func<Exception?>? prelude = _preludes.Count > 0 ? _preludes.Dequeue() : _lastPrelude;
        Func<HttpResponseMessage>? outcome = _outcomes.Count > 0 ? _outcomes.Dequeue() : _last;
        if (_outcomes.Count == 0)
        {
            _lastPrelude = prelude;
            _last = outcome;
        }

        if (prelude?.Invoke() is { } exception)
        {
            throw exception;
        }

        return outcome is null
            ? throw new InvalidOperationException("The mock operation has no scripted outcome.")
            : outcome();
    }

    internal bool HasScript => _outcomes.Count > 0 || _last is not null;

    /// <summary>200 with an approved terminal transaction (transactionStatus 1).</summary>
    public MockOperation ReturnsApproved(
        string transactionId = SyntheticData.TransactionId,
        string merchantTransactionId = SyntheticData.MerchantTransactionId)
        => EnqueueJson(HttpStatusCode.OK, TransactionJson(1, transactionId, merchantTransactionId));

    /// <summary>200 with a declined terminal transaction (transactionStatus 2) — a business outcome, not a failure class.</summary>
    public MockOperation ReturnsDeclined(
        string transactionId = SyntheticData.TransactionId,
        string merchantTransactionId = SyntheticData.MerchantTransactionId)
        => EnqueueJson(HttpStatusCode.OK, TransactionJson(2, transactionId, merchantTransactionId));

    /// <summary>200 with a terminally-failed transaction (transactionStatus 3).</summary>
    public MockOperation ReturnsErrored(
        string transactionId = SyntheticData.TransactionId,
        string merchantTransactionId = SyntheticData.MerchantTransactionId)
        => EnqueueJson(HttpStatusCode.OK, TransactionJson(3, transactionId, merchantTransactionId));

    /// <summary>PermanentRejection row: 400/401/403/404/422 with a structured error body.</summary>
    public MockOperation ReturnsRejected(int statusCode = 422, string error = "synthetic validation rejection")
        => EnqueueJson((HttpStatusCode)statusCode, $"{{\"error\":\"{error}\"}}");

    /// <summary>TransientFailure row: 503 with <c>code: not_processed</c> — provable non-dispatch, safe to fail over.</summary>
    public MockOperation ReturnsNotProcessed503()
        => EnqueueJson(HttpStatusCode.ServiceUnavailable,
            "{\"error\":\"synthetic breaker open; request not dispatched\",\"code\":\"not_processed\"}");

    /// <summary>OutcomeUnknown row: 503 without <c>not_processed</c> (the platform's conservative shape).</summary>
    public MockOperation ReturnsOutcomeUnknown503()
        => EnqueueJson(HttpStatusCode.ServiceUnavailable,
            "{\"error\":\"synthetic upstream failure after dispatch\",\"code\":\"outcome_unknown\"}");

    /// <summary>OutcomeUnknown row: bare 503 with no code at all (edge/WAF shape — OQ-11).</summary>
    public MockOperation ReturnsBare503()
        => EnqueueJson(HttpStatusCode.ServiceUnavailable, "{\"error\":\"synthetic bare 503\"}");

    /// <summary>OutcomeUnknown row: 500.</summary>
    public MockOperation Returns500()
        => EnqueueJson(HttpStatusCode.InternalServerError, "{\"error\":\"synthetic internal error\",\"code\":\"outcome_unknown\"}");

    /// <summary>OutcomeUnknown row: 502 (edge).</summary>
    public MockOperation Returns502()
        => EnqueueJson(HttpStatusCode.BadGateway, "{\"error\":\"synthetic bad gateway\"}");

    /// <summary>OutcomeUnknown row: 504 (edge).</summary>
    public MockOperation Returns504()
        => EnqueueJson(HttpStatusCode.GatewayTimeout, "{\"error\":\"synthetic gateway timeout\"}");

    /// <summary>TransientFailure row: connection refused — provably never sent.</summary>
    public MockOperation ReturnsConnectionRefused()
        => EnqueueThrow(() => new HttpRequestException(
            HttpRequestError.ConnectionError, "synthetic: connection refused"));

    /// <summary>TransientFailure row: DNS failure before the request was accepted.</summary>
    public MockOperation ReturnsDnsFailure()
        => EnqueueThrow(() => new HttpRequestException(
            HttpRequestError.NameResolutionError, "synthetic: name resolution failed"));

    /// <summary>TransientFailure row: TLS failure before the request was accepted.</summary>
    public MockOperation ReturnsTlsFailure()
        => EnqueueThrow(() => new HttpRequestException(
            HttpRequestError.SecureConnectionError, "synthetic: TLS handshake failed"));

    /// <summary>OutcomeUnknown row: deadline exceeded after send.</summary>
    public MockOperation ReturnsTimeoutAfterSend()
        => EnqueueThrow(() => new TaskCanceledException("synthetic: deadline exceeded after send"));

    /// <summary>OutcomeUnknown row: connection reset mid-flight (no never-sent proof).</summary>
    public MockOperation ReturnsResetMidFlight()
        => EnqueueThrow(() => new HttpRequestException(
            HttpRequestError.ResponseEnded, "synthetic: connection reset mid-flight"));

    /// <summary>Reconcile: 404 — the transaction is not yet visible (NotFoundYet signal).</summary>
    public MockOperation ReturnsNotFoundYet()
        => EnqueueJson(HttpStatusCode.NotFound, "{\"error\":\"synthetic: transaction not found\"}");

    /// <summary>Reconcile (post-P-2): 200 with a pending intent reservation.</summary>
    public MockOperation ReturnsPending(string merchantTransactionId = SyntheticData.MerchantTransactionId)
        => EnqueueJson(HttpStatusCode.OK,
            $"{{\"state\":\"pending\",\"merchantTransactionId\":\"{merchantTransactionId}\",\"transactionType\":\"charge\"}}");

    /// <summary>Escape hatch: an arbitrary status/body (synthetic data only — ADR-SDK-020).</summary>
    public MockOperation Returns(HttpStatusCode statusCode, string jsonBody)
        => EnqueueJson(statusCode, jsonBody);

    /// <summary>Escape hatch: an arbitrary transport exception.</summary>
    public MockOperation Throws(Func<Exception> exceptionFactory)
        => EnqueueThrow(exceptionFactory);

    private static string TransactionJson(int status, string transactionId, string merchantTransactionId)
        => $"{{\"transactionId\":\"{transactionId}\",\"transactionStatus\":{status}," +
           $"\"transactionType\":\"charge\",\"merchantTransactionId\":\"{merchantTransactionId}\"," +
           "\"currency\":\"USD\",\"amount\":1999}";

    private MockOperation EnqueueJson(HttpStatusCode statusCode, string jsonBody)
    {
        _preludes.Enqueue(() => null);
        _outcomes.Enqueue(() =>
        {
            var response = new HttpResponseMessage(statusCode)
            {
                Content = new StringContent(jsonBody, Encoding.UTF8, "application/json"),
            };
            response.Headers.TryAddWithoutValidation(
                Transport.RapHeaders.CorrelationId, SyntheticData.CorrelationId);
            return response;
        });
        return this;
    }

    private MockOperation EnqueueThrow(Func<Exception> factory)
    {
        _preludes.Enqueue(() => factory());
        _outcomes.Enqueue(static () => throw new InvalidOperationException("unreachable"));
        return this;
    }
}
