namespace Revaly.Sdk.Transport;

/// <summary>Wire header names used by the runtime.</summary>
public static class RapHeaders
{
    /// <summary>The API version pin header (spec: selectable contract version).</summary>
    public const string ApiVersion = "X-Api-Version";

    /// <summary>
    /// The request correlation header. The platform echoes it on every response
    /// (generating one when the caller sent none); quote it in support tickets — it
    /// joins directly to RAP-core telemetry (DX contract §c). Note: this response
    /// header is platform middleware behaviour not yet documented in the gated spec —
    /// tracked as a platform spec follow-up.
    /// </summary>
    public const string CorrelationId = "X-Correlation-ID";
}
