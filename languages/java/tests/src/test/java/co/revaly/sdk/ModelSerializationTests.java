package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
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
 * (rap-sdk memory: optional-enum write crash; anyOf/oneOf response binding), pinned here as java
 * regression facts.
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
    void oneOfWrapperCannotDiscriminateTerminalBodies() {
        // CORE DEFECT, pinned: the generated oneOf wrapper for the merchant-transaction
        // GET requires exactly one schema match, but its branch models are all-optional
        // under Jackson's lenient binding, so a valid terminal body matches more than one
        // branch and deserialization THROWS on a successful 200. The runtime therefore
        // never uses this wrapper (RapReconciler reads the raw body). If a generator
        // upgrade fixes discrimination, this test fails deliberately — re-evaluate the
        // reconciler's raw-read note and this pin together.
        assertThrows(
                Exception.class,
                () ->
                        mapper.readValue(
                                SyntheticData.transaction(1, TestClient.MTX),
                                GetTransactionByMerchantTransactionId200Response.class));
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
