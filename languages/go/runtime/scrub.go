// The single central scrub function of this runtime (ADR-SDK-020).
//
// Applied to debug logs, wire traces, and any payload surface the SDK emits.
// Scrubbing is by ALLOWLIST — only known-safe identifier/status fields are
// emitted verbatim; every other scalar is replaced with the scrubbed token, so
// schema evolution fails safe. PAN/CVV/PII can never appear because card and
// customer fields are simply not on the list. API keys are additionally
// redacted at the header layer.
//
// The allowlists are a verbatim port of the other runtimes' lists — extending
// them is a reviewed change to the runtime's PCI posture; never add payload
// value fields.
package runtime

import (
	"encoding/json"
	"net/http"
	"sort"
	"strings"
)

// Scrubbed is the replacement token for scrubbed scalar values.
const Scrubbed = "[scrubbed]"

// Redacted is the replacement token for redacted header values.
const Redacted = "[redacted]"

const unparseable = "[unparseable:scrubbed]"

var fieldAllowlist = map[string]bool{
	"transactionid":         true,
	"merchanttransactionid": true,
	"transactiontype":       true,
	"transactionstatus":     true,
	"transactiondate":       true,
	"responsecode":          true,
	"code":                  true,
	"error":                 true,
	"currency":              true,
	"gatewaytype":           true,
	"gatewaytransactionid":  true,
	"gatewayroutingid":      true,
	"correlationid":         true,
	"status":                true,
	"state":                 true,
	"attempts":              true,
}

// Authorization is never emitted, even redacted-by-length — the merchant API
// key must not leak shape or presence into logs (ADR-SDK-020).
var headerAllowlist = map[string]bool{
	"content-type":           true,
	"content-length":         true,
	"user-agent":             true,
	"x-api-version":          true,
	"x-correlation-id":       true,
	"api-supported-versions": true,
}

// ScrubJSON scrubs a JSON payload string. Allowlisted scalar fields pass
// through verbatim, all other scalars are replaced with Scrubbed;
// object/array structure is preserved. Non-JSON input returns a fixed
// placeholder (never the raw text).
func ScrubJSON(payload string) string {
	if strings.TrimSpace(payload) == "" {
		return ""
	}
	var root any
	if err := json.Unmarshal([]byte(payload), &root); err != nil {
		return unparseable
	}
	out, err := json.Marshal(scrubNode(root, false))
	if err != nil {
		return unparseable
	}
	return string(out)
}

// ScrubHeaders scrubs an HTTP header map for tracing. Allowlisted headers pass
// through; everything else (including Authorization) becomes Redacted.
// Multi-valued headers join with commas per RFC 9110 (User-Agent is a
// space-separated product-token list on the wire). Keys come back sorted so
// trace output is stable.
func ScrubHeaders(headers http.Header) map[string]string {
	result := make(map[string]string, len(headers))
	if headers == nil {
		return result
	}
	names := make([]string, 0, len(headers))
	for name := range headers {
		names = append(names, name)
	}
	sort.Slice(names, func(i, j int) bool { return strings.ToLower(names[i]) < strings.ToLower(names[j]) })
	for _, name := range names {
		separator := ", "
		if strings.EqualFold(name, "user-agent") {
			separator = " "
		}
		value := strings.Join(headers[name], separator)
		if headerAllowlist[strings.ToLower(name)] {
			result[name] = value
		} else {
			result[name] = Redacted
		}
	}
	return result
}

func scrubNode(node any, parentKeyAllowlisted bool) any {
	switch typed := node.(type) {
	case []any:
		// Scalars inside arrays keep only their parent key's status.
		out := make([]any, len(typed))
		for i, element := range typed {
			switch element.(type) {
			case map[string]any, []any:
				out[i] = scrubNode(element, parentKeyAllowlisted)
			default:
				if parentKeyAllowlisted {
					out[i] = element
				} else {
					out[i] = Scrubbed
				}
			}
		}
		return out
	case map[string]any:
		out := make(map[string]any, len(typed))
		for key, child := range typed {
			allowlisted := fieldAllowlist[strings.ToLower(key)]
			switch child.(type) {
			case map[string]any, []any:
				out[key] = scrubNode(child, allowlisted)
			default:
				if allowlisted {
					out[key] = child
				} else {
					out[key] = Scrubbed
				}
			}
		}
		return out
	default:
		// Bare scalar root.
		if parentKeyAllowlisted {
			return node
		}
		return Scrubbed
	}
}
