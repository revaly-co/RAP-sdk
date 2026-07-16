namespace Revaly.Sdk.Reconcile;

/// <summary>
/// The caller-bounded polling policy for <c>RapClient.ReconcileAsync</c> — the ONLY loop
/// this SDK owns (ADR-SDK-004). All bounds are explicit constructor arguments: the SDK
/// ships no default attempt counts, budgets, or delays until the OQ-6 telemetry-derived
/// recommendations land (docs/open-items.md — deliberately not invented here). The
/// backoff shape is exponential with jitter.
/// </summary>
public sealed class ReconcilePolicy
{
    /// <summary>
    /// Creates a polling policy. Choose bounds per your risk policy: reconciliation is
    /// how an <c>OutcomeUnknown</c> payment is resolved, so the budget bounds how long
    /// your checkout holds before escalating.
    /// </summary>
    /// <param name="maxAttempts">Maximum GET attempts (≥ 1).</param>
    /// <param name="overallBudget">Total wall-clock budget across all attempts and waits.</param>
    /// <param name="initialDelay">Delay before the second attempt; doubles each attempt (with jitter).</param>
    /// <param name="maxDelay">Optional cap on the per-wait delay; null leaves growth uncapped within the budget.</param>
    public ReconcilePolicy(int maxAttempts, TimeSpan overallBudget, TimeSpan initialDelay, TimeSpan? maxDelay = null)
    {
        if (maxAttempts < 1)
        {
            throw new ArgumentOutOfRangeException(nameof(maxAttempts), "at least one attempt is required");
        }

        if (overallBudget <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(overallBudget), "the overall budget must be positive");
        }

        if (initialDelay < TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(initialDelay), "the initial delay cannot be negative");
        }

        MaxAttempts = maxAttempts;
        OverallBudget = overallBudget;
        InitialDelay = initialDelay;
        MaxDelay = maxDelay;
    }

    /// <summary>Maximum GET attempts.</summary>
    public int MaxAttempts { get; }

    /// <summary>Total wall-clock budget across all attempts and waits.</summary>
    public TimeSpan OverallBudget { get; }

    /// <summary>Delay before the second attempt (exponential growth afterwards).</summary>
    public TimeSpan InitialDelay { get; }

    /// <summary>Optional cap on the per-wait delay.</summary>
    public TimeSpan? MaxDelay { get; }

    /// <summary>Backoff multiplier per attempt ([Proposed] shape; 2.0).</summary>
    public double Multiplier { get; init; } = 2.0;

    /// <summary>Full jitter ratio applied to each wait ([Proposed] shape; ±20%).</summary>
    public double JitterRatio { get; init; } = 0.2;

    internal TimeSpan DelayForAttempt(int completedAttempts)
    {
        if (InitialDelay == TimeSpan.Zero)
        {
            return TimeSpan.Zero;
        }

        var raw = InitialDelay.TotalMilliseconds * Math.Pow(Multiplier, completedAttempts - 1);
        if (MaxDelay is { } cap && raw > cap.TotalMilliseconds)
        {
            raw = cap.TotalMilliseconds;
        }

        var jitterSpan = raw * JitterRatio;
        var jittered = raw + ((Random.Shared.NextDouble() * 2.0) - 1.0) * jitterSpan;
        return TimeSpan.FromMilliseconds(Math.Max(0, jittered));
    }
}
