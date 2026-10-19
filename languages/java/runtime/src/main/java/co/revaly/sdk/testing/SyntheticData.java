package co.revaly.sdk.testing;

/**
 * Synthetic response bodies for the mock transport — SYNTHETIC DATA ONLY (ADR-SDK-020): no real
 * PANs, customers, or keys ever appear here, and no card fields at all (the mock exercises the
 * failover contract, which never needs them).
 */
public final class SyntheticData {

    public static final String DEFAULT_MERCHANT_TRANSACTION_ID = "mtx-synthetic-1";
    public static final String DEFAULT_TRANSACTION_ID = "txn-synthetic-1";

    /**
     * The synthetic edge-firewall tracking reference carried by the edge-rejection row ({@code
     * details.reference}, the shape of the {@code x-azure-ref} header — ADR-SDK-033).
     */
    public static final String EDGE_REFERENCE = "20261016T181449Z-synthetic0000000000000000000000";

    private SyntheticData() {}

    /** A terminal transaction record; {@code transactionStatus} 1=Approved 2=Declined 3=Error. */
    public static String transaction(int transactionStatus, String merchantTransactionId) {
        return "{"
                + "\"transactionId\":\""
                + escape(DEFAULT_TRANSACTION_ID)
                + "\","
                + "\"merchantTransactionId\":\""
                + escape(merchantTransactionId)
                + "\","
                + "\"transactionStatus\":"
                + transactionStatus
                + ","
                + "\"transactionType\":\"Charge\","
                + "\"responseCode\":\"00\","
                + "\"message\":\"synthetic\""
                + "}";
    }

    /** A pending payment intent (post-P-2 shape; {@code state} is the discriminator). */
    public static String pending(String merchantTransactionId) {
        return "{"
                + "\"state\":\"pending\","
                + "\"merchantTransactionId\":\""
                + escape(merchantTransactionId)
                + "\","
                + "\"transactionType\":\"Charge\""
                + "}";
    }

    /** A grouped envelope (the {@code includeAllTransactions=true} shape). */
    public static String transactionGroup(String merchantTransactionId) {
        String item = transaction(1, merchantTransactionId);
        return "{\"transaction\":" + item + ",\"transactions\":[" + item + "]}";
    }

    /** An {@code ErrorResponse} body; pass a null {@code code} to omit the field. */
    public static String errorBody(String error, String code) {
        if (code == null) {
            return "{\"error\":\"" + escape(error) + "\"}";
        }
        return "{\"error\":\"" + escape(error) + "\",\"code\":\"" + escape(code) + "\"}";
    }

    /**
     * The edge firewall's block body (ADR-SDK-033): {@code details.edgeRejection: true} plus the
     * tracking reference; the production edge serves it as {@code text/html}.
     */
    public static String edgeRejectionBody(String reference) {
        return "{\"details\":{\"edgeRejection\":true,\"reference\":\""
                + escape(reference)
                + "\"},\"error\":\"synthetic: blocked by the edge firewall; did not reach the"
                + " payment platform\"}";
    }

    /** The legacy edge HTML block page — not JSON, so no marker can be read. */
    public static String htmlBlockPage() {
        return "<html><head><title>403 Forbidden</title></head>"
                + "<body>synthetic edge block page</body></html>";
    }

    private static String escape(String value) {
        return value == null ? "" : value.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
