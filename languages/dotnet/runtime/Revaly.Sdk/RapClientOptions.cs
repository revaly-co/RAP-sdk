using Microsoft.Extensions.Logging;
using Revaly.Sdk.Logging;

namespace Revaly.Sdk;

/// <summary>
/// Configuration for one <see cref="RapClient"/> (runtime-tdd §1). One client object
/// per configuration; the client is thread-safe and shareable — create it once and
/// reuse it (no global singletons).
/// </summary>
public sealed class RapClientOptions
{
    /// <summary>
    /// The merchant API key (required). Sent as <c>Authorization: ApiKey &lt;key&gt;</c>
    /// on every request; never persisted, never logged, never present in exception
    /// messages (ADR-SDK-020).
    /// </summary>
    public required string ApiKey { get; init; }

    /// <summary>
    /// The API base URL. Defaults to <c>https://api.revaly.co</c> — sandbox and live
    /// share this URL; the environment is selected by your API key's scope, not the URL.
    /// Override only for internal/pre-release targets.
    /// </summary>
    public Uri BaseUrl { get; init; } = new("https://api.revaly.co");

    /// <summary>
    /// The API contract version, pinned via <c>X-Api-Version</c> on every request.
    /// Default <c>"2.1"</c>; <c>"2.0"</c> is selectable.
    /// <b>Behavioural difference on "2.0":</b> the <c>ErrorResponse.code</c> field is not
    /// part of the 2.0 documented contract, so the fast-failover class narrows to
    /// client-provable never-sent failures only — a 503 with <c>code: not_processed</c>
    /// classifies as OutcomeUnknown (reconcile) instead of TransientFailure (immediate
    /// failover). Pin 2.1 unless you have a frozen 2.0 integration.
    /// </summary>
    public string ApiVersion { get; init; } = "2.1";

    /// <summary>
    /// TCP/TLS connection-establishment timeout. Default:
    /// <see cref="DefaultConnectTimeout"/> (10 seconds, ratified from the OQ-11 edge
    /// verification — ADR-SDK-029; ~25× the observed cold client→edge TLS envelope and
    /// 65 s below the overall deadline). Expiry classifies as <b>TransientFailure</b>
    /// (the connect phase is provably never-sent). Set
    /// <see cref="System.Threading.Timeout.InfiniteTimeSpan"/> to disable the SDK bound
    /// and ride the transport's own behaviour (<c>SocketsHttpHandler</c> has no connect
    /// timeout of its own).
    /// </summary>
    public TimeSpan? ConnectTimeout { get; init; }

    /// <summary>
    /// The connect-timeout default applied when <see cref="ConnectTimeout"/> is
    /// unset: 10 seconds (ADR-SDK-029).
    /// </summary>
    public static readonly TimeSpan DefaultConnectTimeout = TimeSpan.FromSeconds(10);

    internal TimeSpan? EffectiveConnectTimeout =>
        ConnectTimeout == System.Threading.Timeout.InfiniteTimeSpan
            ? null
            : ConnectTimeout ?? DefaultConnectTimeout;

    /// <summary>
    /// Overall per-request deadline. Expiry after the request was sent classifies as
    /// <b>OutcomeUnknown</b> (reconcile before acting) — never TransientFailure.
    /// Default: <see cref="DefaultOverallDeadline"/> (75 seconds, ratified from
    /// production latency telemetry — ADR-SDK-027; it clears every observed gateway
    /// tail cluster and clips ≲0.007% of charges). Set
    /// <see cref="System.Threading.Timeout.InfiniteTimeSpan"/> to disable the SDK
    /// deadline and ride the transport's own behaviour (<c>HttpClient</c>'s 100-second
    /// default).
    /// </summary>
    public TimeSpan? OverallDeadline { get; init; }

    /// <summary>
    /// The overall-deadline default applied when <see cref="OverallDeadline"/> is
    /// unset: 75 seconds (ADR-SDK-027).
    /// </summary>
    public static readonly TimeSpan DefaultOverallDeadline = TimeSpan.FromSeconds(75);

    internal TimeSpan? EffectiveOverallDeadline =>
        OverallDeadline == System.Threading.Timeout.InfiniteTimeSpan
            ? null
            : OverallDeadline ?? DefaultOverallDeadline;

    /// <summary>
    /// Logger factory for the ecosystem-native <c>ILogger</c> integration. Default
    /// output is values-free at Information; Debug adds allowlist-scrubbed payloads
    /// (ADR-SDK-020). Null disables SDK logging.
    /// </summary>
    public ILoggerFactory? LoggerFactory { get; init; }

    /// <summary>
    /// Optional request/response observer for Enablement escalations. Receives
    /// payloads already scrubbed by the runtime's central allowlist scrubber — never
    /// raw material. Observer exceptions are swallowed.
    /// </summary>
    public Action<RapWireTrace>? WireTraceHook { get; init; }

    /// <summary>
    /// Replacement wire transport. Intended for the mock transport
    /// (<c>Revaly.Sdk.Testing.RapMockTransport</c>) in merchant tests; null uses the
    /// real HTTP transport.
    /// </summary>
    public HttpMessageHandler? Transport { get; init; }

    internal void Validate()
    {
        if (string.IsNullOrWhiteSpace(ApiKey))
        {
            throw new ArgumentException("ApiKey is required.", nameof(ApiKey));
        }

        if (string.IsNullOrWhiteSpace(ApiVersion))
        {
            throw new ArgumentException("ApiVersion is required.", nameof(ApiVersion));
        }

        if (OverallDeadline is { } deadline
            && deadline != System.Threading.Timeout.InfiniteTimeSpan
            && deadline <= TimeSpan.Zero)
        {
            throw new ArgumentException(
                "OverallDeadline must be positive, or Timeout.InfiniteTimeSpan to disable the SDK deadline.",
                nameof(OverallDeadline));
        }

        if (ConnectTimeout is { } connect
            && connect != System.Threading.Timeout.InfiniteTimeSpan
            && connect <= TimeSpan.Zero)
        {
            throw new ArgumentException(
                "ConnectTimeout must be positive, or Timeout.InfiniteTimeSpan to disable the SDK connect bound.",
                nameof(ConnectTimeout));
        }
    }
}
