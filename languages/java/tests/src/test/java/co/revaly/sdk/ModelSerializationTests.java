package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.model.GetTransactionByMerchantTransactionId200Response;
import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.core.model.PendingTransactionResponse;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.testing.SyntheticData;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

/**
 * Core-serialization probes for the two cross-language generator traps found on the dotnet runtime
 * (optional-enum write crash; anyOf/oneOf response binding), pinned here as java regression facts.
 * The oneOf discrimination defect is FIXED by the oneof_model.mustache template fork — the wrapper
 * tests below pin the forked behaviour (strict pass, coverage tiebreak, both wrappers).
 */
class ModelSerializationTests {

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

    @Test
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
