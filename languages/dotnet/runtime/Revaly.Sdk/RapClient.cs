using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Revaly.Sdk.Core.Api;
using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Extensions;
using Revaly.Sdk.Reconcile;
using Revaly.Sdk.Transport;

namespace Revaly.Sdk;

/// <summary>
/// The RAP V2 client — the one object a merchant constructs (runtime-tdd §1/§2).
/// Exposes the full generated V2 surface (<see cref="Payments"/>,
/// <see cref="PaymentMethods"/>, <see cref="Transactions"/>, <see cref="Notify"/>) plus
/// the <see cref="ReconcileAsync"/> safety helper. Thread-safe and shareable; create one
/// per configuration and reuse it. All requests carry the API key, the
/// <c>X-Api-Version</c> pin, and the ADR-SDK-005 User-Agent, injected at the transport
/// layer where the generated core cannot bypass them. Failures surface exclusively as
/// the three typed exceptions of the failover contract; there are no hidden retries
/// anywhere (ADR-SDK-004).
/// </summary>
public sealed class RapClient : IDisposable
{
    private readonly ServiceProvider _provider;
    private readonly RapReconciler _reconciler;

    /// <summary>Creates a client from <paramref name="options"/>.</summary>
    public RapClient(RapClientOptions options)
    {
        ArgumentNullException.ThrowIfNull(options);
        options.Validate();

        var loggerFactory = options.LoggerFactory ?? NullLoggerFactory.Instance;
        var overallDeadline = options.EffectiveOverallDeadline;
        var services = new ServiceCollection();
        services.AddSingleton(loggerFactory);
        services.AddSingleton(typeof(ILogger<>), typeof(Logger<>));

        services.AddApi(config =>
        {
            // RAP auth is an API key in the Authorization header with the required
            // "ApiKey" prefix (spec securitySchemes). The generated ApiKeyToken defaults
            // to "Bearer " — always overridden here.
            config.AddTokens(new ApiKeyToken(
                options.ApiKey, ClientUtils.ApiKeyHeader.Authorization, prefix: "ApiKey "));

            config.AddApiHttpClients(
                client =>
                {
                    client.BaseAddress = options.BaseUrl;
                    if (overallDeadline is not null)
                    {
                        // The safety handler owns the deadline so expiry is classified
                        // (OutcomeUnknown), not surfaced as a bare timeout.
                        client.Timeout = System.Threading.Timeout.InfiniteTimeSpan;
                    }
                },
                builder =>
                {
                    // Outermost → innermost: observe → identify → pin → classify.
                    builder
                        .AddHttpMessageHandler(() => new ObservabilityHandler(
                            loggerFactory.CreateLogger("Revaly.Sdk"), options.WireTraceHook))
                        .AddHttpMessageHandler(() => new UserAgentHandler())
                        .AddHttpMessageHandler(() => new ApiVersionHandler(options.ApiVersion))
                        .AddHttpMessageHandler(() => new RapSafetyHandler(
                            overallDeadline, options.ApiVersion));

                    builder.ConfigurePrimaryHttpMessageHandler(() => BuildPrimaryHandler(options));
                });
        });

        _provider = services.BuildServiceProvider();
        Payments = _provider.GetRequiredService<IPaymentsApi>();
        PaymentMethods = _provider.GetRequiredService<IPaymentMethodsApi>();
        Transactions = _provider.GetRequiredService<ITransactionsApi>();
        Notify = _provider.GetRequiredService<INotifyApi>();
        _reconciler = new RapReconciler(
            Transactions,
            _provider.GetRequiredService<JsonSerializerOptionsProvider>().Options,
            loggerFactory.CreateLogger("Revaly.Sdk.Reconcile"));
    }

    /// <summary>Payments: charge, authorize, capture, void, refund, refund-cancel.</summary>
    public IPaymentsApi Payments { get; }

    /// <summary>Payment method management.</summary>
    public IPaymentMethodsApi PaymentMethods { get; }

    /// <summary>Transaction lookup and listing.</summary>
    public ITransactionsApi Transactions { get; }

    /// <summary>Notify operations.</summary>
    public INotifyApi Notify { get; }

    /// <summary>
    /// The OutcomeUnknown reconciliation procedure (failover-contract §3): polls
    /// <c>GET /transactions/merchant/{merchantTransactionId}</c> under the caller's
    /// explicit <paramref name="policy"/> until the transaction is visible or the policy
    /// is exhausted. GET-only and side-effect-free. Always branch the returned verdict
    /// with a default case — the verdict set is open for extension (ADR-SDK-009).
    /// </summary>
    /// <param name="merchantTransactionId">The merchant correlation handle sent on the original payment request.</param>
    /// <param name="policy">Caller-bounded polling policy (attempts, budget, backoff).</param>
    /// <param name="cancellationToken">Cancels polling between and during attempts.</param>
    public Task<RapReconcileVerdict> ReconcileAsync(
        string merchantTransactionId, ReconcilePolicy policy, CancellationToken cancellationToken = default)
        => _reconciler.ReconcileAsync(merchantTransactionId, policy, cancellationToken);

    /// <summary>Disposes the client and its pooled transports.</summary>
    public void Dispose() => _provider.Dispose();

    private static HttpMessageHandler BuildPrimaryHandler(RapClientOptions options)
    {
        if (options.Transport is not null)
        {
            return options.Transport;
        }

        var handler = new SocketsHttpHandler();
        if (options.ConnectTimeout is { } connectTimeout)
        {
            handler.ConnectTimeout = connectTimeout;
        }

        return handler;
    }
}
