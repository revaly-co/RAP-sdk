using System.Text.RegularExpressions;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;
using Revaly.Sdk.Transport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// The ADR-SDK-005 User-Agent is a contract with platform dashboards — the exact string
/// is unit-tested per language and the mock transport asserts its presence.
/// </summary>
public partial class UserAgentTests
{
    [GeneratedRegex(@"^revaly-sdk-dotnet/\d+\.\d+\.\d+(-[0-9A-Za-z\.\-]+)? \(\.NET \d+\.\d+\.\d+; (linux|windows|darwin|other)\)$")]
    private static partial Regex UaGrammar();

    [Fact]
    public void Value_matches_the_normative_grammar()
    {
        Assert.Matches(UaGrammar(), RapUserAgent.Value);
    }

    [Fact]
    public void Semver_carries_no_v_prefix_and_no_build_metadata()
    {
        Assert.DoesNotContain("+", RapUserAgent.Semver, StringComparison.Ordinal);
        Assert.False(RapUserAgent.Semver.StartsWith('v'));
    }

    [Fact]
    public async Task Every_request_leads_with_the_sdk_product_token()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        var recorded = Assert.Single(mock.Requests);
        Assert.True(recorded.Headers.TryGetValue("User-Agent", out var userAgent));
        Assert.StartsWith($"revaly-sdk-dotnet/{RapUserAgent.Semver} ", userAgent, StringComparison.Ordinal);
        Assert.Matches(UaGrammar(), userAgent);
    }

    [Fact]
    public async Task The_generated_cores_placeholder_token_is_replaced_not_duplicated()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        var userAgent = mock.Requests[0].Headers["User-Agent"];
        // The core's config injects revaly-sdk-dotnet/0.0.0-unwrapped-core; the transport
        // layer must leave exactly one SDK product token — the runtime's.
        Assert.DoesNotContain("unwrapped-core", userAgent, StringComparison.Ordinal);
        Assert.Equal(1, CountOccurrences(userAgent, "revaly-sdk-dotnet/"));
    }

    private static int CountOccurrences(string haystack, string needle)
    {
        var count = 0;
        var index = 0;
        while ((index = haystack.IndexOf(needle, index, StringComparison.Ordinal)) >= 0)
        {
            count++;
            index += needle.Length;
        }

        return count;
    }
}
