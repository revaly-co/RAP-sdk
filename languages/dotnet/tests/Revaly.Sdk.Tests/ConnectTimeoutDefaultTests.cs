using Revaly.Sdk.Testing;

namespace Revaly.Sdk.Tests;

/// <summary>
/// ADR-SDK-029 connect-timeout-default semantics: unset resolves to the 10-second
/// edge-ratified default, Timeout.InfiniteTimeSpan opts out of any SDK connect bound,
/// explicit values pass through, and zero/negative values are rejected at construction.
/// </summary>
public class ConnectTimeoutDefaultTests
{
    private static RapClientOptions Options(TimeSpan? connectTimeout = null) => new()
    {
        ApiKey = SyntheticData.TestApiKey,
        BaseUrl = new Uri("https://sandbox.synthetic.test"),
        Transport = new RapMockTransport(),
        ConnectTimeout = connectTimeout,
    };

    [Fact]
    public void Unset_resolves_to_the_ratified_default()
    {
        Assert.Equal(TimeSpan.FromSeconds(10), RapClientOptions.DefaultConnectTimeout);
        Assert.Equal(
            RapClientOptions.DefaultConnectTimeout,
            Options().EffectiveConnectTimeout);
    }

    [Fact]
    public void InfiniteTimeSpan_opts_out_of_any_sdk_connect_bound()
    {
        Assert.Null(Options(System.Threading.Timeout.InfiniteTimeSpan).EffectiveConnectTimeout);
    }

    [Fact]
    public void Explicit_values_pass_through_unchanged()
    {
        Assert.Equal(
            TimeSpan.FromSeconds(3),
            Options(TimeSpan.FromSeconds(3)).EffectiveConnectTimeout);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-5)]
    public void Zero_and_negative_connect_timeouts_are_rejected_at_construction(int seconds)
    {
        var ex = Assert.Throws<ArgumentException>(
            () => new RapClient(Options(TimeSpan.FromSeconds(seconds))));
        Assert.Equal(nameof(RapClientOptions.ConnectTimeout), ex.ParamName);
    }
}
