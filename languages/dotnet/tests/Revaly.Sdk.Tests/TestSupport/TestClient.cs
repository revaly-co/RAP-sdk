using Microsoft.Extensions.Logging;
using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Logging;
using Revaly.Sdk.Testing;

namespace Revaly.Sdk.Tests.TestSupport;

/// <summary>Builders shared across the suite — every client here runs on the mock transport.</summary>
public static class TestClient
{
    public static RapClient Create(
        RapMockTransport mock,
        string apiVersion = "2.1",
        ILoggerFactory? loggerFactory = null,
        Action<RapWireTrace>? wireTraceHook = null,
        TimeSpan? overallDeadline = null)
    {
        return new RapClient(new RapClientOptions
        {
            ApiKey = SyntheticData.TestApiKey,
            BaseUrl = new Uri("https://sandbox.synthetic.test"),
            ApiVersion = apiVersion,
            LoggerFactory = loggerFactory,
            WireTraceHook = wireTraceHook,
            Transport = mock,
            OverallDeadline = overallDeadline,
        });
    }

    /// <summary>
    /// A minimal valid charge request carrying the synthetic test card. Optional enums
    /// (paymentMethodType, cardType) are deliberately omitted — the forked
    /// JsonConverter template guards them with Option.IsSet, and
    /// ModelSerializationTests keeps that guard regression-tested.
    /// </summary>
    public static PaymentRequest ChargeRequest(string merchantTransactionId = SyntheticData.MerchantTransactionId)
        => new(
            amount: 1999,
            merchantTransactionId: merchantTransactionId,
            currency: new Option<string?>("USD"),
            paymentMethod: new Option<PaymentMethod?>(new PaymentMethod(
                creditCard: new Option<CreditCard?>(new CreditCard(
                    SyntheticData.TestPan, "12", "2030",
                    cardVerificationCode: new Option<string?>(SyntheticData.TestCvv))))));
}
