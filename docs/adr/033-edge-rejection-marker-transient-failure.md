# ADR-SDK-033 — Edge-rejection marker: a 403 carrying `details.edgeRejection: true` classifies as TransientFailure (RFC-071 D8, OQ6)

**Status:** Accepted — decided 2026-10-18 by Dimitri Pankov as RAP SDK author (RFC-071 open
question 6, ratified at the RFC-071 Gate 2; recorded on SC-660 comment 26805) · amends
ADR-SDK-002 (`details` is no longer wholly opaque: exactly one structured key is read) and
ADR-SDK-029 Decision 1 (the WAF-403 nuance is superseded for marker-bearing bodies) · revises
`failover-contract.md` §2 table, algorithm and Appendix A1 · RFC-046 §5.2 failure table revised
as an RFC revision (the Confluence copy is updated with the release)
**Source:** RFC-071 "Stop WAF false positives blocking merchant transactions" (Backbone,
approved 2026-10-07), decision D8; SC-660 (Epic SC-654); production probe SC-657 (2026-10-16)
**Owner:** SC Eng
**Safety-critical:** yes — this changes the merchant's failover trigger for one response shape

## Context

RFC-071 moves the production edge firewall into a role where it blocks requests it judges
hostile, including merchant transactions (D1). Its D8 decided that a merchant blocked at the
edge receives a **403 with a readable body and a per-operation instruction**, with the `code`
field staying absent on 4xx. SC-657 shipped that body on 2026-10-16 and it was probed in
production the same day (SC-660 comments 26778 and 26779). What the SDK can rely on:

- HTTP status **403**, no `code` field.
- Body (JSON): `{"details":{"edgeRejection":true,"reference":"<tracking reference>"},"error":"<fixed sentence>"}`.
- The marker is `details.edgeRejection`, a JSON boolean `true`.
- `details.reference` is the Front Door tracking reference, equal to the response's
  `x-azure-ref` header and to the firewall log's `trackingReference_s`, in the form
  `YYYYMMDDTHHMMSSZ-<id>`. Each probe's reference matched a firewall `Block` row for that request
  and no origin access row: the request **never reached the payment platform**.
- The body is served as **`Content-Type: text/html`**. Front Door has no setting for the content
  type of a custom block response, so the SDK cannot gate on `application/json`.
- The body is set on the whole policy: every edge block on `api.revaly.co` returns it. The
  platform's own 403s never carry `details.edgeRejection`, so the marker is what tells the two
  apart. The `error` sentence is fixed text and is never read.

Under ADR-SDK-002 and ADR-SDK-029 every 403 classifies as PermanentRejection ("fix or decline,
never fail over"). For an edge block that is wrong on both counts: the payment is definitively
not processed, and the merchant is told to decline a payment the contract would otherwise let
them fail over. The hazard the contract exists to prevent (`failover-contract.md` §1, the double
charge) is not in play: non-dispatch is proven by the platform's own edge, the same class of
proof the SDK already accepts for a refused connection and for `503 {code: "not_processed"}`.

## Decision

In scope order, deliberately isolated:

1. **Classification rule.** One line is added to the normative algorithm, ahead of the 4xx
   line: a 403 whose body parses as JSON, **whatever the `Content-Type`**, and carries
   `details.edgeRejection` equal to the JSON boolean `true` classifies as **TransientFailure**.
   Every other 403 stays PermanentRejection: the legacy HTML block page, a JSON body without the
   marker (or with the key holding anything but the boolean `true`), and the platform's own
   403. The `error` sentence is never read.
2. **No new class.** The three classes of the developer-experience contract (commitments b and
   d) are unchanged. Existing merchant fail-over handlers written against TransientFailure act
   correctly the day they upgrade, with no new branch to write.
3. **Two fields on every typed error:** `isEdgeRejection` (boolean) and `edgeReference` (the
   value of `details.reference`), in each language's idiom. Both are populated only from a
   marker-bearing 403; otherwise `false` and absent. The reference lets a merchant quote the
   exact firewall decision to support.
4. **Per-operation instruction**, carried in the quickstart's TransientFailure branch and in the
   contract prose: **charge and authorize** were never accepted, so the merchant fails over or
   corrects the content and retries; **capture, void, refund and refund-cancel** retry the same
   request.
5. **Reconcile helper.** A marker-bearing 403 on the reconcile read is a transport-class
   failure: polling continues within the caller's policy (before this ADR any non-404
   PermanentRejection ended the loop).
6. **Both API version pins** (2.0 and 2.1) honour the marker: the edge sits in front of the API
   and the marker is not part of `ErrorResponse.code`.
7. **Mock transport** gains one row (403 with the marker, served as `text/html`) and two
   negative controls (403 HTML page; 403 JSON without the marker), in all six languages.
8. **Documents revised with the change:** ADR-SDK-002 (`details` is no longer wholly opaque;
   exactly one structured key is read), ADR-SDK-029 Decision 1 (the "WAF 403 held as
   PermanentRejection" nuance is superseded for marker-bearing bodies), `failover-contract.md`
   §2 table, algorithm, §3 and Appendix A1, and the RFC-046 §5.2 failure table as an RFC
   revision. The developer-experience commitments (a) to (f) do not change.
9. **Release:** a **minor** release of all six packages, cut only after the Backbone
   specification change of SC-660 AC1 (the marker prose in `ErrorResponse.yaml`) is pinned, so
   the generated reference carries the marker's meaning. Irreversible in practice afterwards:
   the platform keeps `details.edgeRejection` and `details.reference` stable on every edge
   block (RFC-071 D8).

## Alternatives considered

- **A fourth top-level class (`EdgeRejection`):** precise, but it breaks the three-class
  promise, falls through existing `switch` statements silently in Go, Java and PHP, and needs a
  major release before any merchant benefits. Rejected.
- **PermanentRejection with a flag:** contradicts D8, which licenses fail-over. Rejected.
- **A per-language subclass of TransientFailure:** deferred; it can be added later as idiom
  sugar without changing the classification.
- **Gating the body parse on `Content-Type: application/json`:** rejected; the edge serves the
  body as `text/html` and that cannot be changed (RFC-071 open question 5).
- **Reading the `error` sentence:** rejected; message strings are not contract (ADR-SDK-002).

## Consequences

- Behaviour change: a merchant blocked at the edge now receives **TransientFailure** (safe to
  fail over) with the firewall reference, instead of PermanentRejection. Nothing else changes.
- Every runtime attempts a JSON parse of every 403 body regardless of content type. A non-JSON
  or marker-less body costs one failed parse and stays PermanentRejection.
- Appendix A1 of the contract narrows "treat `details` as opaque" to "opaque except the one
  structured key named here", and its "edge-generated error bodies are HTML, never
  `ErrorResponse`" is superseded: the edge now mints a JSON body and the SDK reads exactly one
  key of it. The P-1 rule stands: only the platform's `503 {code: "not_processed"}` and this
  marker license fast failover, and classification still never reads message text, latency or
  wait lengths.
- `edgeReference` is a correlation value (it joins the firewall log), not a payload value. In
  this release it is exposed on the typed error only: the values-free log lines and the
  debug-level scrubber allowlists are unchanged (the `details` object stays `[scrubbed]` in wire
  traces), so the PCI posture of ADR-SDK-020 does not move.
- Ships as a minor release ×6 after the AC1 pin (Decision 9). Until then `main` carries the
  change unreleased.
- The ADR-SDK-029 Decision 3 ops guardrail extends to the block body: changing the marker key,
  the reference token or the status of the edge block response changes merchant-visible SDK
  behaviour and must be flagged to the SDK owners before rollout.

## Implementation guidance

Classification algorithm (normative pseudocode; implement idiomatically per language):

```
classify(outcome):
  if transport error and request provably never sent          → TransientFailure
  if HTTP status == 403 and body parses as JSON (any Content-Type)
     and body.details.edgeRejection == true (JSON boolean)    → TransientFailure   [this ADR]
  if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
  if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
  if HTTP status >= 500                                       → OutcomeUnknown
  if deadline exceeded after send, or connection reset,
     or response unreadable/ambiguous                         → OutcomeUnknown
```

- The marker test is exact: a failed parse, a non-object body, a missing or non-object
  `details`, or an `edgeRejection` value that is not the JSON boolean `true` (the string
  `"true"`, the number `1`, `null`) all mean "no marker".
- `edgeReference` is `details.reference` when it is a string, otherwise absent. It is never an
  input to classification.
- The 403 body is parsed once; the same parse feeds `code` (absent on 4xx), the message and the
  opaque `details` passthrough.
- The reconcile helper treats a marker-bearing 403 on its GET exactly like a transport failure
  or a 5xx: record the attempt (status 403, correlation id) and keep polling within the policy.
