namespace Revaly.Sdk.Transport;

/// <summary>
/// Injects the ADR-SDK-005 User-Agent at the transport layer, where the generated core
/// cannot bypass it. Merchant frameworks may APPEND their own product token after the
/// SDK's; the SDK prefix stays first and intact so platform segmentation keeps working,
/// and there is deliberately no way to replace or suppress it.
/// </summary>
internal sealed class UserAgentHandler : DelegatingHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var appended = request.Headers.UserAgent
            .Where(t => t.Product?.Name != RapUserAgent.ProductName)
            .ToList();

        request.Headers.UserAgent.Clear();
        request.Headers.UserAgent.Add(RapUserAgent.ProductToken);
        request.Headers.UserAgent.Add(RapUserAgent.CommentToken);
        foreach (var token in appended)
        {
            request.Headers.UserAgent.Add(token);
        }

        return base.SendAsync(request, cancellationToken);
    }
}
