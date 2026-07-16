using System.Net.Http.Headers;
using System.Reflection;

namespace Revaly.Sdk.Transport;

/// <summary>
/// Builds the adoption-telemetry User-Agent per the ADR-SDK-005 normative grammar:
/// <c>revaly-sdk-dotnet/&lt;semver&gt; (.NET &lt;runtime-version&gt;; &lt;os&gt;)</c>.
/// The exact string is a contract with platform dashboards; it carries only the coarse
/// tokens below — no hostnames, no distro fingerprints.
/// </summary>
public static class RapUserAgent
{
    /// <summary>The fixed lowercase language token (ADR-SDK-005 grammar).</summary>
    public const string ProductName = "revaly-sdk-dotnet";

    /// <summary>The package semver, no <c>v</c> prefix (stage 5 stamps release versions).</summary>
    public static string Semver { get; } = ResolveSemver();

    /// <summary>Coarse runtime identifier, e.g. <c>.NET 10.0.3</c>.</summary>
    public static string RuntimeVersion { get; } = $".NET {Environment.Version}";

    /// <summary>Coarse platform token: <c>linux</c> / <c>windows</c> / <c>darwin</c> / <c>other</c>.</summary>
    public static string Os { get; } = ResolveOs();

    /// <summary>The full header value, e.g. <c>revaly-sdk-dotnet/1.2.0 (.NET 10.0.3; linux)</c>.</summary>
    public static string Value { get; } = $"{ProductName}/{Semver} ({RuntimeVersion}; {Os})";

    /// <summary>The product token part (<c>revaly-sdk-dotnet/&lt;semver&gt;</c>).</summary>
    public static ProductInfoHeaderValue ProductToken { get; } = new(ProductName, Semver);

    /// <summary>The comment token part (<c>(.NET &lt;version&gt;; &lt;os&gt;)</c>).</summary>
    public static ProductInfoHeaderValue CommentToken { get; } = new($"({RuntimeVersion}; {Os})");

    private static string ResolveSemver()
    {
        var informational = typeof(RapUserAgent).Assembly
            .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion;
        if (string.IsNullOrWhiteSpace(informational))
        {
            return "0.0.0";
        }

        // Strip build metadata (+sha) — the ADR grammar carries the bare semver.
        var plus = informational.IndexOf('+', StringComparison.Ordinal);
        return plus > 0 ? informational[..plus] : informational;
    }

    private static string ResolveOs()
    {
        if (OperatingSystem.IsWindows())
        {
            return "windows";
        }

        if (OperatingSystem.IsLinux())
        {
            return "linux";
        }

        if (OperatingSystem.IsMacOS())
        {
            return "darwin";
        }

        return "other";
    }
}
