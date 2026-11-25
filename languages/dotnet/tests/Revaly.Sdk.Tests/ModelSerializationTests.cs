using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// Regression coverage for the forked generichost JsonConverter template
/// (pipeline/dotnet/templates/libraries/generichost/JsonConverter.mustache): optional
/// inner enums must be guarded by Option.IsSet — the stock template dereferenced the
/// unset Option and crashed any request that omitted them. Also pins the listTransactions
/// oneOf wrapper (ListTransactions200ResponseInner): each row binds its own branch, and an
/// unknown additive field never moves it.
/// </summary>
public class ModelSerializationTests
{
    private const string FlatRow =
        "{\"transactionId\":\"t-1\",\"transactionDate\":\"2025-09-13T03:19:54.86Z\",\"transactionStatus\":1," +
        "\"responseCode\":\"10000\",\"transactionType\":\"Charge\",\"amount\":2500,\"currencyCode\":\"USD\"}";

    private const string PaymentMethodRow =
        "{\"transaction\":{\"transactionId\":\"t-2\",\"transactionDate\":\"2025-12-02T14:44:42.209Z\"," +
        "\"transactionStatus\":1,\"message\":\"Succeeded!\",\"responseCode\":\"10000\"," +
        "\"transactionType\":\"CreateCreditCard\",\"paymentMethod\":{\"paymentMethodId\":\"pm-1\"," +
        "\"lastFourDigits\":\"1111\",\"firstSixDigits\":\"411111\",\"cardType\":\"VISA\"," +
        "\"storageState\":\"Cached\",\"issuerIdentificationNumber\":\"41111111\"}}}";

    private static string WithAdditiveField(string row) => row[..^1] + ",\"futureAdditiveField\":\"x\"}";

    private static async Task<List<ListTransactions200ResponseInner>> ListTransactionsAsync(params string[] rows)
    {
        var mock = new RapMockTransport();
        mock.Stub(HttpMethod.Get, "/transactions")
            .Returns(System.Net.HttpStatusCode.OK, "[" + string.Join(",", rows) + "]");
        using var client = TestClient.Create(mock);

        var response = await client.Transactions.ListTransactionsAsync();

        // Ok(), not TryOk(): a converter failure must surface here, not log and return false.
        var items = response.Ok();
        Assert.NotNull(items);
        return items;
    }

    [Fact]
    public async Task List_transactions_binds_a_flat_row_to_TransactionListItem()
    {
        var item = Assert.Single(await ListTransactionsAsync(FlatRow));

        Assert.Null(item.TransactionListPaymentMethodItem);
        var row = Assert.IsType<TransactionListItem>(item.TransactionListItem);
        Assert.Equal("t-1", row.TransactionId);
        Assert.Equal(new DateTime(2025, 9, 13, 3, 19, 54, 860, DateTimeKind.Utc), row.TransactionDate);
        Assert.Equal(1, row.TransactionStatus);
        Assert.Equal("10000", row.ResponseCode);
        Assert.Equal("Charge", row.TransactionType);
        Assert.Equal(2500L, row.Amount);
        Assert.Equal("USD", row.CurrencyCode);
    }

    [Fact]
    public async Task List_transactions_binds_a_payment_method_row_to_TransactionListPaymentMethodItem()
    {
        var item = Assert.Single(await ListTransactionsAsync(PaymentMethodRow));

        Assert.Null(item.TransactionListItem);
        var transaction = Assert.IsType<TransactionListPaymentMethodItem>(item.TransactionListPaymentMethodItem).Transaction;
        Assert.Equal("t-2", transaction.TransactionId);
        Assert.Equal(new DateTime(2025, 12, 2, 14, 44, 42, 209, DateTimeKind.Utc), transaction.TransactionDate);
        Assert.Equal(1, transaction.TransactionStatus);
        Assert.Equal("Succeeded!", transaction.Message);
        Assert.Equal("10000", transaction.ResponseCode);
        Assert.Equal("CreateCreditCard", transaction.TransactionType);
        var paymentMethod = Assert.IsType<TransactionListPaymentMethod>(transaction.PaymentMethod);
        Assert.Equal("pm-1", paymentMethod.PaymentMethodId);
        Assert.Equal("1111", paymentMethod.LastFourDigits);
        Assert.Equal("411111", paymentMethod.FirstSixDigits);
        Assert.Equal("VISA", paymentMethod.CardType);
        Assert.Equal("Cached", paymentMethod.StorageState);
    }

    [Fact]
    public async Task List_transactions_keeps_a_flat_row_with_an_unknown_additive_field_on_TransactionListItem()
    {
        var item = Assert.Single(await ListTransactionsAsync(WithAdditiveField(FlatRow)));

        Assert.Null(item.TransactionListPaymentMethodItem);
        Assert.Equal("t-1", Assert.IsType<TransactionListItem>(item.TransactionListItem).TransactionId);
    }

    [Fact]
    public async Task List_transactions_keeps_a_payment_method_row_with_an_unknown_additive_field_on_TransactionListPaymentMethodItem()
    {
        var item = Assert.Single(await ListTransactionsAsync(WithAdditiveField(PaymentMethodRow)));

        Assert.Null(item.TransactionListItem);
        var transaction = Assert.IsType<TransactionListPaymentMethodItem>(item.TransactionListPaymentMethodItem).Transaction;
        Assert.Equal("t-2", transaction.TransactionId);
        Assert.Equal("1111", Assert.IsType<TransactionListPaymentMethod>(transaction.PaymentMethod).LastFourDigits);
    }

    [Fact]
    public async Task List_transactions_decodes_a_mixed_page_to_each_rows_own_branch()
    {
        var items = await ListTransactionsAsync(FlatRow, PaymentMethodRow);

        Assert.Collection(items,
            flat => Assert.Equal("t-1", Assert.IsType<TransactionListItem>(flat.TransactionListItem).TransactionId),
            pm => Assert.Equal("t-2", Assert.IsType<TransactionListPaymentMethodItem>(pm.TransactionListPaymentMethodItem).Transaction.TransactionId));
    }

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
