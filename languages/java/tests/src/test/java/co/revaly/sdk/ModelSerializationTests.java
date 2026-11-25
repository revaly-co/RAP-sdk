package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.model.GetTransactionByMerchantTransactionId200Response;
import co.revaly.sdk.core.model.ListTransactions200ResponseInner;
import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.core.model.PendingTransactionResponse;
import co.revaly.sdk.core.model.TransactionListItem;
import co.revaly.sdk.core.model.TransactionListPaymentMethodItem;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.testing.SyntheticData;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * Core-serialization probes for the two cross-language generator traps found on the dotnet runtime
 * (optional-enum write crash; anyOf/oneOf response binding), pinned here as java regression facts.
 * The oneOf discrimination defect is FIXED by the oneof_model.mustache template fork — the wrapper
 * tests below pin the forked behaviour (strict pass, coverage tiebreak, all three wrappers).
 */
class ModelSerializationTests {

    // GET /transactions row shapes (spec v2.19.0): the flat TransactionListItem and the
    // nested TransactionListPaymentMethodItem. Synthetic values only (ADR-SDK-020).
    private static final String FLAT_ROW =
            "{\"transactionId\":\"t-1\",\"transactionDate\":\"2025-09-13T03:19:54.86Z\","
                    + "\"transactionStatus\":1,\"responseCode\":\"10000\","
                    + "\"transactionType\":\"Charge\",\"amount\":2500,\"currencyCode\":\"USD\"}";
    private static final String PAYMENT_METHOD_ROW =
            "{\"transaction\":{\"transactionId\":\"t-2\","
                    + "\"transactionDate\":\"2025-12-02T14:44:42.209Z\",\"transactionStatus\":1,"
                    + "\"message\":\"Succeeded!\",\"responseCode\":\"10000\","
                    + "\"transactionType\":\"CreateCreditCard\",\"paymentMethod\":{"
                    + "\"paymentMethodId\":\"pm-1\",\"lastFourDigits\":\"1111\","
                    + "\"firstSixDigits\":\"411111\",\"cardType\":\"VISA\","
                    + "\"storageState\":\"Cached\",\"issuerIdentificationNumber\":\"41111111\"}}}";

    private final ObjectMapper mapper = ApiClient.createDefaultObjectMapper();

    @Test
    void optionalInnerEnumOmittedSerializesCleanly() throws Exception {
        // The dotnet generichost core crashed serializing an OPTIONAL inner enum left
        // unset (fixed by template fork, PR #15). The java native core uses
        // Jackson + JsonNullable — prove the defect mechanism is absent here.
        String json = mapper.writeValueAsString(TestClient.paymentRequest());

        assertFalse(json.contains("paymentMethodType"), "undefined optional stays absent");
        assertTrue(json.contains(TestClient.MTX));
    }

    // EnumOrdinal is intentional here: any generated constant exercises the serializer, and
    // values()[0] deliberately avoids pinning a spec-specific enum NAME that a regeneration
    // could drop — the test is order-independent by design.
    @Test
    @SuppressWarnings("EnumOrdinal")
    void optionalInnerEnumPresentSerializesItsWireValue() throws Exception {
        PaymentRequest.PaymentMethodTypeEnum first =
                PaymentRequest.PaymentMethodTypeEnum.values()[0];
        String json =
                mapper.writeValueAsString(TestClient.paymentRequest().paymentMethodType(first));

        assertTrue(json.contains("\"paymentMethodType\":\"" + first.getValue() + "\""));
    }

    @Test
    void oneOfWrapperDiscriminatesTerminalBodies() throws Exception {
        // Fixed 2026-07-16 via the oneof_model.mustache template fork (strict first
        // pass + coverage tiebreak): stock upstream demanded exactly one LENIENT match,
        // which all-optional branch models can never provide — valid 200s threw. The
        // reconciler still reads raw bodies by design (repo rule 5); these pins keep the
        // re-exported transaction GETs honest.
        GetTransactionByMerchantTransactionId200Response wrapper =
                mapper.readValue(
                        SyntheticData.transaction(1, TestClient.MTX),
                        GetTransactionByMerchantTransactionId200Response.class);

        assertEquals(1, wrapper.getTransactionResponse().getTransactionStatus());
    }

    @Test
    void oneOfWrapperDiscriminatesPendingBodies() throws Exception {
        GetTransactionByMerchantTransactionId200Response wrapper =
                mapper.readValue(
                        SyntheticData.pending(TestClient.MTX),
                        GetTransactionByMerchantTransactionId200Response.class);

        assertEquals(
                PendingTransactionResponse.StateEnum.PENDING,
                wrapper.getPendingTransactionResponse().getState());
    }

    @Test
    void oneOfWrapperDiscriminatesGroupEnvelopes() throws Exception {
        GetTransactionByMerchantTransactionId200Response wrapper =
                mapper.readValue(
                        SyntheticData.transactionGroup(TestClient.MTX),
                        GetTransactionByMerchantTransactionId200Response.class);

        assertEquals(
                TestClient.MTX,
                wrapper.getTransactionGroupResponse().getTransaction().getMerchantTransactionId());
    }

    @Test
    void oneOfWrapperSurvivesAdditiveServerFields() throws Exception {
        // A server newer than the pinned spec sends fields this SDK does not know
        // (the statementDescriptor precedent). Every strict attempt fails, so the
        // coverage tiebreak must bind the branch recognizing the most fields instead
        // of throwing.
        String terminalPlusUnknown =
                SyntheticData.transaction(2, TestClient.MTX)
                        .replaceFirst("\\{", "{\"futureAdditiveField\":\"x\",");

        GetTransactionByMerchantTransactionId200Response wrapper =
                mapper.readValue(
                        terminalPlusUnknown,
                        GetTransactionByMerchantTransactionId200Response.class);

        assertEquals(2, wrapper.getTransactionResponse().getTransactionStatus());
    }

    @Test
    void byIdWrapperDiscriminatesToo() throws Exception {
        // Same forked deserializer, second affected wrapper (GET /transactions/{id}).
        co.revaly.sdk.core.model.GetTransactionById200Response wrapper =
                mapper.readValue(
                        SyntheticData.transaction(1, TestClient.MTX),
                        co.revaly.sdk.core.model.GetTransactionById200Response.class);

        assertEquals(1, wrapper.getTransactionResponse().getTransactionStatus());
    }

    @Test
    void listItemWrapperDiscriminatesFlatRows() throws Exception {
        // Same forked deserializer, third wrapper: the GET /transactions array items.
        ListTransactions200ResponseInner wrapper =
                mapper.readValue(FLAT_ROW, ListTransactions200ResponseInner.class);

        TransactionListItem row =
                assertInstanceOf(TransactionListItem.class, wrapper.getActualInstance());
        assertEquals("t-1", row.getTransactionId());
        assertEquals(
                Instant.parse("2025-09-13T03:19:54.86Z"), row.getTransactionDate().toInstant());
        assertEquals(1, row.getTransactionStatus());
        assertEquals("10000", row.getResponseCode());
        assertEquals("Charge", row.getTransactionType());
        assertEquals(2500L, row.getAmount());
        assertEquals("USD", row.getCurrencyCode());
    }

    @Test
    void listItemWrapperDiscriminatesPaymentMethodRows() throws Exception {
        ListTransactions200ResponseInner wrapper =
                mapper.readValue(PAYMENT_METHOD_ROW, ListTransactions200ResponseInner.class);

        TransactionListPaymentMethodItem row =
                assertInstanceOf(
                        TransactionListPaymentMethodItem.class, wrapper.getActualInstance());
        assertEquals("t-2", row.getTransaction().getTransactionId());
        assertEquals(1, row.getTransaction().getTransactionStatus());
        assertEquals("CreateCreditCard", row.getTransaction().getTransactionType());
        assertEquals("1111", row.getTransaction().getPaymentMethod().getLastFourDigits());
    }

    @Test
    void listItemWrapperSurvivesAdditiveFieldsOnFlatRows() throws Exception {
        // Both strict attempts fail; the coverage tiebreak must still bind the flat branch.
        String flatPlusUnknown = FLAT_ROW.replaceFirst("\\{", "{\"futureAdditiveField\":\"x\",");

        ListTransactions200ResponseInner wrapper =
                mapper.readValue(flatPlusUnknown, ListTransactions200ResponseInner.class);

        TransactionListItem row =
                assertInstanceOf(TransactionListItem.class, wrapper.getActualInstance());
        assertEquals("t-1", row.getTransactionId());
    }

    @Test
    void listItemWrapperSurvivesAdditiveFieldsOnPaymentMethodRows() throws Exception {
        String paymentMethodPlusUnknown =
                PAYMENT_METHOD_ROW.replaceFirst("\\{", "{\"futureAdditiveField\":\"x\",");

        ListTransactions200ResponseInner wrapper =
                mapper.readValue(paymentMethodPlusUnknown, ListTransactions200ResponseInner.class);

        TransactionListPaymentMethodItem row =
                assertInstanceOf(
                        TransactionListPaymentMethodItem.class, wrapper.getActualInstance());
        assertEquals("1111", row.getTransaction().getPaymentMethod().getLastFourDigits());
    }

    @Test
    void listTransactionsArrayDecodesEachRowToItsBranch() throws Exception {
        // The generated listTransactions decodes its 200 body with exactly this TypeReference.
        List<ListTransactions200ResponseInner> rows =
                mapper.readValue(
                        "[" + FLAT_ROW + "," + PAYMENT_METHOD_ROW + "]",
                        new TypeReference<List<ListTransactions200ResponseInner>>() {});

        assertEquals(2, rows.size());
        TransactionListItem flat =
                assertInstanceOf(TransactionListItem.class, rows.get(0).getActualInstance());
        TransactionListPaymentMethodItem nested =
                assertInstanceOf(
                        TransactionListPaymentMethodItem.class, rows.get(1).getActualInstance());
        assertEquals("t-1", flat.getTransactionId());
        assertEquals("t-2", nested.getTransaction().getTransactionId());
    }

    @Test
    void listItemWrapperBindsAMalformedPaymentMethodRowAsAnEmptyFlatRow() throws Exception {
        // KNOWN EDGE, pinned so a fork revision flips it deliberately (precedent: ADR-SDK-034
        // §3). A payment-method row the nested branch cannot decode (here a non-numeric
        // transactionStatus) leaves the flat branch as the only lenient match — it accepts any
        // object, because its one required member is nullable and not enforced on read — and
        // the fork binds a single lenient match without the strict/coverage pass. The row
        // comes back as an EMPTY TransactionListItem, not an error; .NET and Go raise instead.
        String malformed =
                PAYMENT_METHOD_ROW.replace(
                        "\"transactionStatus\":1", "\"transactionStatus\":\"x\"");

        ListTransactions200ResponseInner wrapper =
                mapper.readValue(malformed, ListTransactions200ResponseInner.class);

        TransactionListItem row =
                assertInstanceOf(TransactionListItem.class, wrapper.getActualInstance());
        assertNull(row.getTransactionId());
    }

    @Test
    void terminalBodyBindsDirectlyToTransactionResponse() throws Exception {
        // The runtime's chosen path: direct class-level bind, no wrapper.
        TransactionResponse transaction =
                mapper.readValue(
                        SyntheticData.transaction(1, TestClient.MTX), TransactionResponse.class);

        assertEquals(1, transaction.getTransactionStatus());
        assertEquals(TestClient.MTX, transaction.getMerchantTransactionId());
    }

    @Test
    void pendingBodyBindsDirectlyToPendingTransactionResponse() throws Exception {
        PendingTransactionResponse pending =
                mapper.readValue(
                        SyntheticData.pending(TestClient.MTX), PendingTransactionResponse.class);

        assertEquals(PendingTransactionResponse.StateEnum.PENDING, pending.getState());
        assertEquals(TestClient.MTX, pending.getMerchantTransactionId());
    }

    @Test
    void unknownStateValueFallsToOpenEnumDefault() throws Exception {
        // enumUnknownDefaultCase (ADR-SDK-023 §A3): new wire values must never throw.
        PendingTransactionResponse pending =
                mapper.readValue(
                        "{\"state\":\"reserved\",\"merchantTransactionId\":\""
                                + TestClient.MTX
                                + "\"}",
                        PendingTransactionResponse.class);

        assertNotNull(pending.getState());
        assertEquals(
                PendingTransactionResponse.StateEnum.UNKNOWN_DEFAULT_OPEN_API, pending.getState());
    }
}
