using System.Text.Json;
using System.Text.Json.Nodes;

namespace Revaly.Sdk.Logging;

/// <summary>
/// The single central scrub function of this runtime (ADR-SDK-020): applied to debug
/// logs, wire traces, and any payload surface the SDK emits. Scrubbing is by
/// ALLOWLIST — only known-safe identifier/status fields are emitted verbatim; every
/// other scalar is replaced with <c>"[scrubbed]"</c>, so schema evolution fails safe.
/// PAN/CVV/PII can never appear because card and customer fields are simply not on
/// the list. API keys are additionally redacted at the header layer.
/// </summary>
public static class RapScrubber
{
    /// <summary>The replacement token for scrubbed scalar values.</summary>
    public const string Scrubbed = "[scrubbed]";

    /// <summary>The replacement token for redacted header values.</summary>
    public const string Redacted = "[redacted]";

    // Known-safe fields: identifiers, statuses and routing metadata designed for
    // support tickets and telemetry joins. Deliberately absent: every cardholder,
    // customer, address and amount field. Extending this list is a reviewed change
    // to the runtime's PCI posture — never add payload value fields.
    private static readonly HashSet<string> FieldAllowlist = new(StringComparer.OrdinalIgnoreCase)
    {
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
        "attempts",
    };

    // Known-safe headers. Authorization is never emitted, even redacted-by-length —
    // the merchant API key must not leak shape or presence into logs (ADR-SDK-020).
    private static readonly HashSet<string> HeaderAllowlist = new(StringComparer.OrdinalIgnoreCase)
    {
        "Content-Type",
        "Content-Length",
        "User-Agent",
        Transport.RapHeaders.ApiVersion,
        Transport.RapHeaders.CorrelationId,
        "api-supported-versions",
    };

    /// <summary>
    /// Scrubs a JSON payload: allowlisted scalar fields pass through verbatim, all other
    /// scalars are replaced with <see cref="Scrubbed"/>; object/array structure is
    /// preserved. Non-JSON input returns a fixed placeholder (never the raw text).
    /// </summary>
    public static string ScrubJson(string? payload)
    {
        if (string.IsNullOrWhiteSpace(payload))
        {
            return string.Empty;
        }

        JsonNode? root;
        try
        {
            root = JsonNode.Parse(payload);
        }
        catch (JsonException)
        {
            return "[unparseable:scrubbed]";
        }

        var scrubbed = ScrubNode(root, parentKeyAllowlisted: false);
        return scrubbed?.ToJsonString(new JsonSerializerOptions { WriteIndented = false }) ?? Scrubbed;
    }

    /// <summary>
    /// Scrubs an HTTP header set for tracing: allowlisted headers pass through,
    /// everything else (including <c>Authorization</c>) becomes <see cref="Redacted"/>.
    /// </summary>
    public static IReadOnlyDictionary<string, string> ScrubHeaders(
        IEnumerable<KeyValuePair<string, IEnumerable<string>>> headers)
    {
        var result = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var (name, headerValues) in headers)
        {
            result[name] = HeaderAllowlist.Contains(name)
                ? string.Join(", ", headerValues)
                : Redacted;
        }

        return result;
    }

    private static JsonNode? ScrubNode(JsonNode? node, bool parentKeyAllowlisted)
    {
        switch (node)
        {
            case JsonObject obj:
                var newObj = new JsonObject();
                foreach (var (key, child) in obj)
                {
                    newObj[key] = child is JsonValue
                        ? (FieldAllowlist.Contains(key) ? child.DeepClone() : JsonValue.Create(Scrubbed))
                        : ScrubNode(child, FieldAllowlist.Contains(key));
                }

                return newObj;

            case JsonArray array:
                var newArray = new JsonArray();
                foreach (var element in array)
                {
                    // Scalars inside arrays keep only their parent key's status.
                    newArray.Add(element is JsonValue
                        ? (parentKeyAllowlisted ? element.DeepClone() : JsonValue.Create(Scrubbed))
                        : ScrubNode(element, parentKeyAllowlisted));
                }

                return newArray;

            case JsonValue value:
                return parentKeyAllowlisted ? value.DeepClone() : JsonValue.Create(Scrubbed);

            default:
                return null;
        }
    }
}
