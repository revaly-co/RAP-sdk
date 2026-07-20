using Revaly.Sdk.Testing;

namespace Revaly.Sdk.Tests;

/// <summary>
/// ADR-SDK-027 deadline-default semantics: unset resolves to the 30-second ratified
/// default, Timeout.InfiniteTimeSpan opts out of any SDK deadline, explicit values pass
/// through, and zero/negative values are rejected at construction.
/// </summary>
public class DeadlineDefaultTests
{
    private static RapClientOptions Options(TimeSpan? overallDeadline = null) => new()
    {
        ApiKey = SyntheticData.TestApiKey,
        BaseUrl = new Uri("https://sandbox.synthetic.test"),
        Transport = new RapMockTransport(),
        OverallDeadline = overallDeadline,
    };

    [Fact]
    public void Unset_resolves_to_the_ratified_30s_default()
    {
        Assert.Equal(TimeSpan.FromSeconds(30), RapClientOptions.DefaultOverallDeadline);
        Assert.Equal(
            RapClientOptions.DefaultOverallDeadline,
            Options().EffectiveOverallDeadline);
    }

    [Fact]
    public void InfiniteTimeSpan_opts_out_of_any_sdk_deadline()
    {
        Assert.Null(Options(System.Threading.Timeout.InfiniteTimeSpan).EffectiveOverallDeadline);
    }

    [Fact]
    public void Explicit_values_pass_through_unchanged()
    {
        Assert.Equal(
            TimeSpan.FromSeconds(5),
            Options(TimeSpan.FromSeconds(5)).EffectiveOverallDeadline);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-5)]
    public void Zero_and_negative_deadlines_are_rejected_at_construction(int seconds)
    {
        var ex = Assert.Throws<ArgumentException>(
            () => new RapClient(Options(TimeSpan.FromSeconds(seconds))));
        Assert.Equal(nameof(RapClientOptions.OverallDeadline), ex.ParamName);
    }
}
