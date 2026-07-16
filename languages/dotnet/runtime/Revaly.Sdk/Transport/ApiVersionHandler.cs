namespace Revaly.Sdk.Transport;

/// <summary>
/// Pins <c>X-Api-Version</c> on every request (runtime-tdd §1). A version already set
/// on the request (an explicit per-call choice through the core surface) is respected;
/// otherwise the client's configured pin is applied — requests never leave version-less,
/// because an absent header binds to the base contract <c>2.0</c> server-side.
/// </summary>
internal sealed class ApiVersionHandler : DelegatingHandler
{
    private readonly string _apiVersion;

    internal ApiVersionHandler(string apiVersion)
    {
        _apiVersion = apiVersion;
    }

    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        if (!request.Headers.Contains(RapHeaders.ApiVersion))
        {
            request.Headers.TryAddWithoutValidation(RapHeaders.ApiVersion, _apiVersion);
        }

        return base.SendAsync(request, cancellationToken);
    }
}
