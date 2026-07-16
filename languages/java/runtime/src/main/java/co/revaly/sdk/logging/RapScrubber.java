package co.revaly.sdk.logging;

import co.revaly.sdk.transport.RapHeaders;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

/**
 * The single central scrub function of this runtime (ADR-SDK-020): applied to debug logs, wire
 * traces, and any payload surface the SDK emits. Scrubbing is by ALLOWLIST — only known-safe
 * identifier/status fields are emitted verbatim; every other scalar is replaced with {@code
 * "[scrubbed]"}, so schema evolution fails safe. PAN/CVV/PII can never appear because card and
 * customer fields are simply not on the list. API keys are additionally redacted at the header
 * layer.
 */
public final class RapScrubber {

    /** The replacement token for scrubbed scalar values. */
    public static final String SCRUBBED = "[scrubbed]";

    /** The replacement token for redacted header values. */
    public static final String REDACTED = "[redacted]";

    private static final ObjectMapper MAPPER = new ObjectMapper();

    // Known-safe fields: identifiers, statuses and routing metadata designed for support
    // tickets and telemetry joins. Deliberately absent: every cardholder, customer,
    // address and amount field. Extending this list is a reviewed change to the runtime's
    // PCI posture — never add payload value fields.
    private static final Set<String> FIELD_ALLOWLIST =
            caseInsensitiveSet(
                    "transactionId",
                    "merchantTransactionId",
                    "transactionType",
                    "transactionStatus",
                    "transactionDate",
                    "responseCode",
                    "code",
                    "error",
                    "currency",
                    "gatewayType",
                    "gatewayTransactionId",
                    "gatewayRoutingId",
                    "correlationId",
                    "status",
                    "state",
                    "attempts");

    // Known-safe headers. Authorization is never emitted, even redacted-by-length — the
    // merchant API key must not leak shape or presence into logs (ADR-SDK-020).
    private static final Set<String> HEADER_ALLOWLIST =
            caseInsensitiveSet(
                    "Content-Type",
                    "Content-Length",
                    RapHeaders.USER_AGENT,
                    RapHeaders.API_VERSION,
                    RapHeaders.CORRELATION_ID,
                    "api-supported-versions");

    private RapScrubber() {}

    /**
     * Scrubs a JSON payload: allowlisted scalar fields pass through verbatim, all other scalars are
     * replaced with {@link #SCRUBBED}; object/array structure is preserved. Non-JSON input returns
     * a fixed placeholder (never the raw text).
     */
    public static String scrubJson(String payload) {
        if (payload == null || payload.trim().isEmpty()) {
            return "";
        }

        JsonNode root;
        try {
            root = MAPPER.readTree(payload);
        } catch (IOException e) {
            return "[unparseable:scrubbed]";
        }

        JsonNode scrubbed = scrubNode(root, false);
        return scrubbed == null ? SCRUBBED : scrubbed.toString();
    }

    /**
     * Scrubs an HTTP header set for tracing: allowlisted headers pass through, everything else
     * (including {@code Authorization}) becomes {@link #REDACTED}. User-Agent is a space-separated
     * product-token list on the wire; other multi-valued headers join with commas per RFC 9110.
     */
    public static Map<String, String> scrubHeaders(Map<String, List<String>> headers) {
        Map<String, String> result = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
        if (headers == null) {
            return result;
        }
        for (Map.Entry<String, List<String>> entry : headers.entrySet()) {
            String name = entry.getKey();
            if (name == null) {
                continue;
            }
            if (HEADER_ALLOWLIST.contains(name)) {
                String separator = RapHeaders.USER_AGENT.equalsIgnoreCase(name) ? " " : ", ";
                result.put(name, String.join(separator, entry.getValue()));
            } else {
                result.put(name, REDACTED);
            }
        }
        return result;
    }

    private static JsonNode scrubNode(JsonNode node, boolean parentKeyAllowlisted) {
        if (node == null) {
            return null;
        }
        if (node.isObject()) {
            ObjectNode newObj = MAPPER.createObjectNode();
            Iterator<Map.Entry<String, JsonNode>> fields = node.fields();
            while (fields.hasNext()) {
                Map.Entry<String, JsonNode> field = fields.next();
                String key = field.getKey();
                JsonNode child = field.getValue();
                boolean allowlisted = FIELD_ALLOWLIST.contains(key);
                if (child.isValueNode()) {
                    if (allowlisted) {
                        newObj.set(key, child.deepCopy());
                    } else {
                        newObj.put(key, SCRUBBED);
                    }
                } else {
                    newObj.set(key, scrubNode(child, allowlisted));
                }
            }
            return newObj;
        }
        if (node.isArray()) {
            ArrayNode newArray = MAPPER.createArrayNode();
            for (JsonNode element : node) {
                if (element.isValueNode()) {
                    // Scalars inside arrays keep only their parent key's status.
                    if (parentKeyAllowlisted) {
                        newArray.add(element.deepCopy());
                    } else {
                        newArray.add(SCRUBBED);
                    }
                } else {
                    newArray.add(scrubNode(element, parentKeyAllowlisted));
                }
            }
            return newArray;
        }
        // Bare scalar root.
        return parentKeyAllowlisted ? node.deepCopy() : MAPPER.getNodeFactory().textNode(SCRUBBED);
    }

    private static Set<String> caseInsensitiveSet(String... values) {
        Set<String> set = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
        for (String value : values) {
            set.add(value);
        }
        return set;
    }
}
