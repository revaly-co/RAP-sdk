package co.revaly.sdk.testing;

/**
 * Synthetic response bodies for the mock transport — SYNTHETIC DATA ONLY (ADR-SDK-020): no real
 * PANs, customers, or keys ever appear here, and no card fields at all (the mock exercises the
 * failover contract, which never needs them).
 */
public final class SyntheticData {

    public static final String DEFAULT_MERCHANT_TRANSACTION_ID = "mtx-synthetic-1";
    public static final String DEFAULT_TRANSACTION_ID = "txn-synthetic-1";

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

    private static String escape(String value) {
        return value == null ? "" : value.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
