namespace Revaly.Sdk.Testing;

/// <summary>One request observed by the mock transport, for merchant test assertions.</summary>
/// <param name="Method">The HTTP method.</param>
/// <param name="Path">The request path.</param>
/// <param name="Headers">A snapshot of the request headers.</param>
/// <param name="Body">The request body, when present.</param>
public sealed record RecordedRequest(
    string Method,
    string Path,
    IReadOnlyDictionary<string, string> Headers,
    string? Body);
