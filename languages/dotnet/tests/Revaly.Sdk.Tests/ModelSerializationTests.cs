using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// Regression coverage for the forked generichost JsonConverter template
/// (pipeline/dotnet/templates/libraries/generichost/JsonConverter.mustache): optional
/// inner enums must be guarded by Option.IsSet — the stock template dereferenced the
/// unset Option and crashed any request that omitted them.
/// </summary>
public class ModelSerializationTests
{
    [Fact]
    public async Task Optional_enums_may_be_omitted_and_stay_off_the_wire()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        // ChargeRequest omits paymentMethodType and cardType entirely.
        var response = await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        Assert.True(response.TryOk(out _));
        var body = Assert.Single(mock.Requests).Body!;
        Assert.DoesNotContain("paymentMethodType", body, StringComparison.Ordinal);
        Assert.DoesNotContain("cardType", body, StringComparison.Ordinal);
    }

    [Fact]
    public async Task Optional_enums_serialize_their_wire_values_when_set()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        var request = new PaymentRequest(
            amount: 1999,
            merchantTransactionId: SyntheticData.MerchantTransactionId,
            paymentMethodType: new Option<PaymentRequest.PaymentMethodTypeEnum?>(
                PaymentRequest.PaymentMethodTypeEnum.CreditCard),
            currency: new Option<string?>("USD"),
            paymentMethod: new Option<PaymentMethod?>(new PaymentMethod(
                creditCard: new Option<CreditCard?>(new CreditCard(
                    SyntheticData.TestPan, "12", "2030",
                    cardVerificationCode: new Option<string?>(SyntheticData.TestCvv),
                    cardType: new Option<CreditCard.CardTypeEnum?>(CreditCard.CardTypeEnum.Visa))))));

        await client.Payments.ChargePaymentAsync(request);

        var body = Assert.Single(mock.Requests).Body!;
        Assert.Contains("\"paymentMethodType\":\"creditCard\"", body, StringComparison.Ordinal);
        Assert.Contains("\"cardType\":\"visa\"", body, StringComparison.Ordinal);
    }
}
