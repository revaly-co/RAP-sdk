using Revaly.Sdk.Logging;
using Revaly.Sdk.Testing;

namespace Revaly.Sdk.Tests;

/// <summary>
/// The central allowlist scrubber (ADR-SDK-020): tested against a full charge payload,
/// not a field list that can drift — unknown fields must fail safe (scrubbed).
/// </summary>
public class ScrubberTests
{
    [Fact]
    public void Card_material_never_survives_scrubbing()
    {
        var payload = $"{{\"amount\":1999,\"merchantTransactionId\":\"{SyntheticData.MerchantTransactionId}\"," +
            $"\"currency\":\"USD\",\"paymentMethod\":{{\"creditCard\":{{\"number\":\"{SyntheticData.TestPan}\"," +
            $"\"expiryMonth\":\"12\",\"expiryYear\":\"2030\",\"cardVerificationCode\":\"{SyntheticData.TestCvv}\"}}}}," +
            "\"customerIp\":\"203.0.113.9\",\"description\":\"synthetic order\"}";

        var scrubbed = RapScrubber.ScrubJson(payload);

        Assert.DoesNotContain(SyntheticData.TestPan, scrubbed, StringComparison.Ordinal);
        Assert.DoesNotContain(SyntheticData.TestCvv, scrubbed, StringComparison.Ordinal);
        Assert.DoesNotContain("203.0.113.9", scrubbed, StringComparison.Ordinal);
        Assert.DoesNotContain("1999", scrubbed, StringComparison.Ordinal);
        Assert.Contains(SyntheticData.MerchantTransactionId, scrubbed, StringComparison.Ordinal);
        Assert.Contains("USD", scrubbed, StringComparison.Ordinal);
        Assert.Contains(RapScrubber.Scrubbed, scrubbed, StringComparison.Ordinal);
    }

    [Fact]
    public void Unknown_future_fields_fail_safe()
    {
        var scrubbed = RapScrubber.ScrubJson(
            "{\"someNewField\":\"secret-value\",\"transactionId\":\"txn_1\"}");

        Assert.DoesNotContain("secret-value", scrubbed, StringComparison.Ordinal);
        Assert.Contains("txn_1", scrubbed, StringComparison.Ordinal);
    }

    [Fact]
    public void Non_json_input_returns_a_placeholder_never_the_raw_text()
    {
        var scrubbed = RapScrubber.ScrubJson("PAN=4111111111111111 raw text");

        Assert.DoesNotContain("4111111111111111", scrubbed, StringComparison.Ordinal);
        Assert.Equal("[unparseable:scrubbed]", scrubbed);
    }

    [Fact]
    public void Authorization_headers_are_redacted_even_in_traces()
    {
        var headers = new Dictionary<string, IEnumerable<string>>
        {
            ["Authorization"] = new[] { $"ApiKey {SyntheticData.TestApiKey}" },
            ["X-Api-Version"] = new[] { "2.1" },
            ["X-Custom"] = new[] { "anything" },
        };

        var scrubbed = RapScrubber.ScrubHeaders(headers);

        Assert.Equal(RapScrubber.Redacted, scrubbed["Authorization"]);
        Assert.Equal("2.1", scrubbed["X-Api-Version"]);
        Assert.Equal(RapScrubber.Redacted, scrubbed["X-Custom"]);
    }

    [Fact]
    public void Arrays_and_nested_structures_are_preserved_but_scrubbed()
    {
        var scrubbed = RapScrubber.ScrubJson(
            "{\"items\":[{\"number\":\"4111111111111111\"},{\"transactionId\":\"txn_2\"}]}");

        Assert.DoesNotContain("4111111111111111", scrubbed, StringComparison.Ordinal);
        Assert.Contains("txn_2", scrubbed, StringComparison.Ordinal);
    }
}
