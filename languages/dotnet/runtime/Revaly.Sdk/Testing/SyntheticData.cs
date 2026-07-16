namespace Revaly.Sdk.Testing;

/// <summary>
/// The synthetic fixtures used by the mock transport. Mock mode uses ONLY synthetic
/// data (ADR-SDK-020) — never recorded live payloads. The PAN below is the standard
/// industry test number; it exists here so merchants (and our own log-capture tests)
/// can assert that card material never reaches logs.
/// </summary>
public static class SyntheticData
{
    /// <summary>The standard Visa test PAN. Synthetic — never a real card.</summary>
    public const string TestPan = "4111111111111111";

    /// <summary>A synthetic CVV.</summary>
    public const string TestCvv = "123";

    /// <summary>A synthetic API key for tests; asserting its absence from logs is the log-capture test's job.</summary>
    public const string TestApiKey = "sk_synthetic_test_0123456789";

    /// <summary>A synthetic transaction id.</summary>
    public const string TransactionId = "txn_synthetic_0001";

    /// <summary>A synthetic merchant transaction id (the reconcile correlation handle).</summary>
    public const string MerchantTransactionId = "mtx_synthetic_0001";

    /// <summary>The synthetic correlation id stamped on every mock response.</summary>
    public const string CorrelationId = "corr_synthetic_0001";
}
