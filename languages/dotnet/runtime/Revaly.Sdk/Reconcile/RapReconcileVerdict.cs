using Revaly.Sdk.Core.Model;

namespace Revaly.Sdk.Reconcile;

/// <summary>
/// The reconcile verdict hierarchy (failover-contract §3; ADR-SDK-009). V1 produces
/// exactly two verdicts — <see cref="FoundVerdict"/> and <see cref="NotFoundYetVerdict"/> —
/// and the hierarchy is deliberately OPEN FOR EXTENSION: <c>SafeToFailover</c> arrives
/// with platform P-2 as a minor release. Every <c>switch</c> over a verdict MUST carry a
/// default branch that treats the unrecognized verdict conservatively (hold / escalate),
/// exactly as the quickstart shows.
/// </summary>
public abstract class RapReconcileVerdict
{
    private protected RapReconcileVerdict()
    {
    }
}

/// <summary>
/// The transaction is visible at RAP-core. Inspect <see cref="Outcome"/>:
/// terminal outcomes mean the platform owns the result (approved ⇒ done, no failover —
/// the money moved; declined/error ⇒ merchant decision); <see cref="RapTransactionOutcome.Pending"/>
/// (post-P-2 intent reservation) means keep polling.
/// </summary>
public sealed class FoundVerdict : RapReconcileVerdict
{
    internal FoundVerdict(
        RapTransactionOutcome outcome,
        TransactionResponse? transaction,
        PendingTransactionResponse? pending,
        string? correlationId)
    {
        Outcome = outcome;
        Transaction = transaction;
        Pending = pending;
        CorrelationId = correlationId;
    }

    /// <summary>The coarse outcome classification (open set — treat unmapped values via default branches).</summary>
    public RapTransactionOutcome Outcome { get; }

    /// <summary>The full transaction record, when the platform returned a terminal transaction.</summary>
    public TransactionResponse? Transaction { get; }

    /// <summary>The pending intent-reservation record (post-P-2), when the platform returned one.</summary>
    public PendingTransactionResponse? Pending { get; }

    /// <summary>The correlation id of the reconcile response, when present.</summary>
    public string? CorrelationId { get; }

    /// <summary>True when the outcome is terminal (approved/declined/error) — the platform owns the result.</summary>
    public bool IsTerminal => Outcome is RapTransactionOutcome.Approved
        or RapTransactionOutcome.Declined
        or RapTransactionOutcome.Error;
}

/// <summary>
/// The transaction is not yet visible at RAP-core. In V1 this is NEVER proof of
/// absence — platform visibility is asynchronous and unbounded, widest exactly when
/// RAP-core is degraded. Hold and re-poll with backoff; on sustained NotFoundYet,
/// escalate per merchant policy. A merchant who fails over anyway does so in their own
/// code against their own risk policy — the SDK does not bless it.
/// </summary>
public sealed class NotFoundYetVerdict : RapReconcileVerdict
{
    internal NotFoundYetVerdict(int attempts, TimeSpan elapsed, string? lastCorrelationId, int? lastHttpStatus)
    {
        Attempts = attempts;
        Elapsed = elapsed;
        LastCorrelationId = lastCorrelationId;
        LastHttpStatus = lastHttpStatus;
    }

    /// <summary>How many GET attempts the helper made within the caller's policy.</summary>
    public int Attempts { get; }

    /// <summary>Total wall-clock time spent polling.</summary>
    public TimeSpan Elapsed { get; }

    /// <summary>The correlation id of the last reconcile response, for support tickets.</summary>
    public string? LastCorrelationId { get; }

    /// <summary>The HTTP status of the last poll attempt (404 when simply not visible yet).</summary>
    public int? LastHttpStatus { get; }
}
