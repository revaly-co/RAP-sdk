namespace Revaly.Sdk.Reconcile;

/// <summary>
/// Coarse outcome classification of a found transaction, mapped from the platform's
/// documented <c>transactionStatus</c> (1 = Approved, 2 = Declined, 3 = Error) plus the
/// pending intent-reservation state (post-P-2). Values outside the documented set map to
/// <see cref="Unknown"/> — always branch with a default (the set is open; the raw
/// <c>TransactionResponse</c> stays available on the verdict).
/// </summary>
public enum RapTransactionOutcome
{
    /// <summary>The platform reports a state this SDK version does not recognize — treat conservatively.</summary>
    Unknown = 0,

    /// <summary>The payment succeeded at RAP-core. Do not fail over — the money moved.</summary>
    Approved = 1,

    /// <summary>The payment was declined at RAP-core (terminal). Failing over is the merchant's decision.</summary>
    Declined = 2,

    /// <summary>The payment terminally failed at RAP-core. Failing over is the merchant's decision.</summary>
    Error = 3,

    /// <summary>A pending intent reservation is visible (post-P-2). Keep polling.</summary>
    Pending = 4,
}
