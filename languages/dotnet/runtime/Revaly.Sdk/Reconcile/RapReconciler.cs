using System.Diagnostics;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using Revaly.Sdk.Core.Api;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Errors;
using Revaly.Sdk.Transport;

namespace Revaly.Sdk.Reconcile;

/// <summary>
/// The OutcomeUnknown reconciliation procedure (failover-contract §3): GET-only,
/// side-effect-free, caller-bounded — the only loop the runtime owns (ADR-SDK-004).
/// </summary>
internal sealed class RapReconciler
{
    private readonly ITransactionsApi _transactions;
    private readonly JsonSerializerOptions _coreJsonOptions;
    private readonly ILogger _logger;

    internal RapReconciler(ITransactionsApi transactions, JsonSerializerOptions coreJsonOptions, ILogger logger)
    {
        _transactions = transactions;
        _coreJsonOptions = coreJsonOptions;
        _logger = logger;
    }

    internal async Task<RapReconcileVerdict> ReconcileAsync(
        string merchantTransactionId, ReconcilePolicy policy, CancellationToken cancellationToken)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(merchantTransactionId);
        ArgumentNullException.ThrowIfNull(policy);

        var stopwatch = Stopwatch.StartNew();
        var attempts = 0;
        string? lastCorrelationId = null;
        int? lastHttpStatus = null;

        while (true)
        {
            cancellationToken.ThrowIfCancellationRequested();
            attempts++;

            try
            {
                var response = await _transactions
                    .GetTransactionByMerchantTransactionIdAsync(
                        merchantTransactionId, cancellationToken: cancellationToken)
                    .ConfigureAwait(false);

                lastHttpStatus = (int)response.StatusCode;
                lastCorrelationId = response.Headers.TryGetValues(RapHeaders.CorrelationId, out var values)
                    ? values.FirstOrDefault()
                    : lastCorrelationId;

                if (response.TryOk(out var wrapper) && wrapper is not null)
                {
                    // Pending discrimination happens on the RAW body: the anyOf wrapper
                    // tries TransactionResponse first, whose members are all optional, so
                    // a pending body ({state, merchantTransactionId, ...}) would mis-bind
                    // to an empty TransactionResponse. `state` exists only on the pending
                    // schema, so its presence is authoritative.
                    if (TryReadPending(response.RawContent) is { } pending)
                    {
                        return new FoundVerdict(
                            RapTransactionOutcome.Pending, transaction: null, pending, lastCorrelationId);
                    }

                    if (wrapper.TransactionResponse is { } transaction)
                    {
                        return new FoundVerdict(
                            MapOutcome(transaction.TransactionStatus), transaction, pending: null, lastCorrelationId);
                    }

                    // A response shape this SDK version does not recognize (e.g. a
                    // transaction group, or a post-P-2 variant). Found-but-unmapped is
                    // still FOUND — surface it conservatively rather than polling on.
                    return new FoundVerdict(
                        RapTransactionOutcome.Unknown, transaction: null, pending: null, lastCorrelationId);
                }

                // 2xx that did not deserialize: ambiguous read — poll again within budget.
                _logger.LogWarning(
                    "RAP reconcile attempt {Attempt} returned {StatusCode} with an unreadable body; continuing within policy",
                    attempts, lastHttpStatus);
            }
            catch (PermanentRejectionException ex) when (ex.StatusCode == 404)
            {
                // Not yet visible — the NotFoundYet signal, not an error (§3).
                lastHttpStatus = 404;
                lastCorrelationId = ex.CorrelationId ?? lastCorrelationId;
            }
            catch (TransientFailureException ex)
            {
                // The platform provably did not process this READ; the write status is
                // still unknown — keep polling within the caller's budget.
                lastHttpStatus = ex.StatusCode ?? lastHttpStatus;
                lastCorrelationId = ex.CorrelationId ?? lastCorrelationId;
            }
            catch (OutcomeUnknownException ex)
            {
                // Degraded read path (5xx/timeout on the GET) — exactly the window where
                // visibility is widest; keep polling within the caller's budget.
                lastHttpStatus = ex.StatusCode ?? lastHttpStatus;
                lastCorrelationId = ex.CorrelationId ?? lastCorrelationId;
            }

            // PermanentRejection other than 404 (400/401/403/422) escapes: polling will
            // never fix a rejected read (bad credentials, malformed id) — the caller
            // must see it.

            if (attempts >= policy.MaxAttempts)
            {
                break;
            }

            var delay = policy.DelayForAttempt(attempts);
            if (stopwatch.Elapsed + delay >= policy.OverallBudget)
            {
                break;
            }

            if (delay > TimeSpan.Zero)
            {
                await Task.Delay(delay, cancellationToken).ConfigureAwait(false);
            }
        }

        return new NotFoundYetVerdict(attempts, stopwatch.Elapsed, lastCorrelationId, lastHttpStatus);
    }

    private PendingTransactionResponse? TryReadPending(string rawContent)
    {
        try
        {
            using var document = JsonDocument.Parse(rawContent);
            if (document.RootElement.ValueKind != JsonValueKind.Object
                || !document.RootElement.TryGetProperty("state", out var state)
                || state.ValueKind != JsonValueKind.String)
            {
                return null;
            }

            return JsonSerializer.Deserialize<PendingTransactionResponse>(rawContent, _coreJsonOptions);
        }
        catch (JsonException)
        {
            return null;
        }
        catch (NotImplementedException)
        {
            // The core's open-enum StateEnumFromString throws on genuinely unknown
            // state values; a pending-shaped record with an unknown state is still a
            // sighting — the caller maps it via the Unknown outcome path.
            return null;
        }
    }

    private static RapTransactionOutcome MapOutcome(int? transactionStatus) => transactionStatus switch
    {
        1 => RapTransactionOutcome.Approved,
        2 => RapTransactionOutcome.Declined,
        3 => RapTransactionOutcome.Error,
        _ => RapTransactionOutcome.Unknown,
    };
}
