using Revaly.Sdk.Transport;

namespace Revaly.Sdk.Testing;

/// <summary>
/// The first-class no-network test double (DX contract §d): plug it into
/// <see cref="RapClientOptions.Transport"/> and script outcomes with the taxonomy-named
/// builders. Simulates every row of the failover-contract §2 table, both reconcile
/// verdicts and the post-P-2 pending state, and supports scripting consecutive outcomes
/// so merchants can unit-test their failover handler with no network. Asserts on every
/// request that the ADR-SDK-005 User-Agent is present. Synthetic data only (ADR-SDK-020).
/// </summary>
public sealed class RapMockTransport : HttpMessageHandler
{
    private readonly List<(HttpMethod Method, string PathPrefix, MockOperation Operation)> _routes = new();
    private readonly List<RecordedRequest> _requests = new();
    private readonly object _gate = new();

    /// <summary>
    /// Verify on every request that the SDK User-Agent product token leads the header
    /// (on by default — it is part of the contract with platform dashboards).
    /// </summary>
    public bool AssertUserAgent { get; init; } = true;

    /// <summary>Every request observed by the mock, in order.</summary>
    public IReadOnlyList<RecordedRequest> Requests
    {
        get
        {
            lock (_gate)
            {
                return _requests.ToArray();
            }
        }
    }

    /// <summary>Scripts <c>POST /payments</c> (charge).</summary>
    public MockOperation Charge() => Stub(HttpMethod.Post, "/payments");

    /// <summary>Scripts <c>POST /payments/authorize</c>.</summary>
    public MockOperation Authorize() => Stub(HttpMethod.Post, "/payments/authorize");

    /// <summary>Scripts the reconcile GET for one merchant transaction id.</summary>
    public MockOperation Reconcile(string merchantTransactionId)
        => Stub(HttpMethod.Get, $"/transactions/merchant/{merchantTransactionId}");

    /// <summary>Scripts an arbitrary (method, path-prefix) route; the longest matching prefix wins.</summary>
    public MockOperation Stub(HttpMethod method, string pathPrefix)
    {
        lock (_gate)
        {
            foreach (var route in _routes)
            {
                if (route.Method == method && string.Equals(route.PathPrefix, pathPrefix, StringComparison.Ordinal))
                {
                    return route.Operation;
                }
            }

            var operation = new MockOperation();
            _routes.Add((method, pathPrefix, operation));
            return operation;
        }
    }

    /// <inheritdoc />
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var path = request.RequestUri?.AbsolutePath ?? string.Empty;
        var body = request.Content is null
            ? null
            : await request.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);

        var headers = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var (name, values) in request.Headers)
        {
            // User-Agent is a space-separated product-token list on the wire; other
            // multi-valued headers join with commas per RFC 9110.
            headers[name] = string.Join(
                string.Equals(name, "User-Agent", StringComparison.OrdinalIgnoreCase) ? " " : ", ",
                values);
        }

        MockOperation operation;
        lock (_gate)
        {
            _requests.Add(new RecordedRequest(request.Method.Method, path, headers, body));

            if (AssertUserAgent)
            {
                var lead = request.Headers.UserAgent.FirstOrDefault();
                if (lead?.Product?.Name != RapUserAgent.ProductName)
                {
                    throw new InvalidOperationException(
                        $"The SDK User-Agent product token must lead every request (ADR-SDK-005); saw '{request.Headers.UserAgent}'.");
                }
            }

            var match = _routes
                .Where(r => r.Method == request.Method
                    && path.StartsWith(r.PathPrefix, StringComparison.Ordinal))
                .OrderByDescending(r => r.PathPrefix.Length)
                .FirstOrDefault();

            operation = match.Operation ?? throw new InvalidOperationException(
                $"Unscripted request: {request.Method} {path}. Script it with Stub()/Charge()/Reconcile().");
        }

        return operation.Next();
    }
}
