# ADR-SDK-034 — An SDK does not refuse a request for a string length bound; the platform decides (OQ-18)

**Status:** Accepted — decided 2026-11-05 by Dimitri Pankov as RAP SDK author (OQ-18, raised on
PR #118 by the fresh-context review of 2026-11-03, SC-869) · closes OQ-18 · implemented
2026-11-05 (SC-886, see Implementation below) · no failover-contract
change: a request the SDK no longer refuses is sent and classified like any other request
**Amendment:** accepted 2026-11-26 by Dimitri Pankov as RAP SDK author (SC-1018, closes OQ-19):
decision 2 no longer applies to the `rtnData` block in the Python and PHP SDKs. See
[Amendment](#amendment--2026-11-26-sc-1018-python-and-php-do-not-refuse-or-rewrite-rtndata-values-before-sending)
below. Implemented 2026-11-26 under SC-1018 (see
[Implementation (SC-1018)](#implementation-sc-1018) below); Python and PHP will release it as a
patch.
**Source:** spec pins v2.15.0+693a36b (SC-869: the 256-character `description` bound from SC-785)
and v2.16.0+99cb098 (SC-661: the 45-character `customerIp` bound)
**Owner:** SC Eng
**Safety-critical:** no — a client-side length refusal happens before anything is sent, and the
platform's own answer to an over-long value (truncation, or a 400) is already classified by
`failover-contract.md` §2

## Context

The spec declares a `maxLength` on many request strings. For some of them the platform does not
refuse a longer value:

- `description` on charge and authorize is bounded at 256 characters since spec v2.13.1 (SC-785).
  The spec states that a longer value is truncated to its first 256 characters and never blocks
  the payment.
- `customerIp` on charge and authorize is bounded at 45 characters since spec v2.16.0 (SC-661).
  The platform's handling depends on the route today: Olympus declines a value over 45
  characters (code 50037), the direct path accepts up to 50, and Backbone's own contract check
  records the bound without refusing while a 30-day census runs (2026-11-04 to 2026-12-04).

The six generated cores treat the same bound differently:

| Core | What happens to a value over `maxLength` |
| --- | --- |
| Python | Refused when the model is built or a field is assigned (pydantic `max_length`); nothing is sent |
| PHP | Refused in the field's setter (`InvalidArgumentException`); the array constructor does not check and nothing calls `valid()` |
| .NET | Sent: the model implements `IValidatableObject`, but nothing in the core or runtime calls `Validate` |
| Java, TypeScript, Go | Sent: no length check is generated on model fields |

Path parameters are a separate case: Go, Python and PHP check a path parameter's `maxLength` in
the API layer (for example `transactionId` at 50 and `merchantTransactionId` at 100 on capture,
void, refund and refund-cancel); .NET, Java and TypeScript do not.

So a request with a 300-character description is refused before sending in two SDKs and
accepted, truncated, in four. After the v2.16.0 pin, a 46-character `customerIp` would be
refused by Python and PHP before sending, while the direct path accepts it. The SC-661 change
(Backbone PR #439) asked that RAP-sdk not re-pin to 2.16.0 with the client-side 45-character
limit until the field's census closes.

OQ-18 asked (a) whether the Python and PHP refusal is acceptable or the platform should drop
`maxLength` from the spec, and (b) which version the next release takes.

## Decision

1. **No client-side length refusal.** An SDK does not refuse a request before sending because a
   string is longer than a `maxLength` the spec declares. The platform is the single authority:
   it truncates, records or refuses, and a refusal comes back as the platform's own response,
   classified by the failover contract as today.
2. **Scope: `maxLength` on request body fields only.** Path-parameter checks (Go, Python and
   PHP), required fields, patterns, enum values, numeric ranges and `minLength` keep their
   generated checks; this ADR does not change them.
   The spec keeps its bounds: they document the contract, and asking the platform to drop
   them (OQ-18's alternative) is not pursued.
3. **Implementation: a Python and PHP template revision** (SC-886; ADR-SDK-023, like the `oneOf` forks)
   that stops emitting the `maxLength` check, with a test per language proving a value over the
   bound is sent. Python's `test_merchant_transaction_id_max_length_100` asserts today's
   refusal and changes with the revision. The unused .NET `Validate` stays as generated.
4. **Release gate until the revision lands.** Python and PHP are not released from a pin that
   adds or tightens a `maxLength` the platform does not enforce. The v2.16.0 release therefore
   ships .NET, Java, TypeScript and Go only; Python and PHP release with the template revision.
   This relaxes the SC-661 request above: the re-pin lands on `main` with the 45-character check
   in the unreleased Python and PHP cores, and this gate keeps it out of every published package
   (decided by Dimitri Pankov, SC-661 owner, 2026-11-05).
5. **Versions (OQ-18 b): a minor bump per package.** .NET, Java, TypeScript and Go go from 0.8.0
   to 0.9.0 with the v2.16.0 pin. With the template revision, Python goes from 0.8.0 to 0.9.0 and
   PHP from 0.9.1 to 0.10.0. The SDKs are pre-1.0 and the major tracks the RAP V2 API major
   (`pipeline-and-release.md` §4); the platform's breaking-change gate allowlisted the tightened
   `description` bound and reported the `customerIp` bound as a warning, not an error; the
   `merchantTrustLevel` reorder keeps source compatibility and breaks binary
   compatibility in .NET only. Precedent: v0.8.0 (ADR-SDK-033). The classification rationale is
   recorded in each annotated release tag.
6. **Release notes.** The .NET note states the `merchantTrustLevel` renumbering: `NOTTRUSTED`
   moves from 2 to 4, 2 now means `MODERATELYTRUSTED`, and the `UnknownDefaultOpenApi` sentinel
   moves from 4 to 5 (so a stored 4 now reads as `NOTTRUSTED`); recompiled code is unaffected, while
   code compiled against an earlier core, or a stored integer, sends the wrong level. Every note
   describes the bounds as the spec states them (a `description` over 256 characters is
   truncated to its first 256 and never blocks the payment; `customerIp` is IPv4 or IPv6 text of
   at most 45 characters) and does not describe platform enforcement plans.

## Consequences

- Once the revision lands, a request body behaves the same in all six SDKs: it is sent, and the
  platform decides. Path parameters keep their per-language checks.
- A merchant learns of an over-long value from the platform: a truncated `description` is
  silent by the platform's contract, and an enforced bound comes back as the platform's refusal.
- A future pin that adds or tightens a `maxLength` needs no per-language decision once the
  revision lands. Until then, decision 4 applies to every pin.
- Python and PHP are one release behind until the revision ships; their next release carries
  every pin change since v2.13.0.
- No released package refuses a longer `customerIp` before sending, which is what the SC-661
  request protects; `main` carries the check in the unreleased Python and PHP cores until the
  revision.

## Implementation (2026-11-05, SC-886)

- **PHP:** `pipeline/php/templates/model_generic.mustache` is the stock v7.23.0 template with
  only the two `maxLength` blocks removed (the setter's exception and the
  `listInvalidProperties()` entry). 37 model files change, removals only.
- **Python: a generation step, not a template fork.** The generator hands the model template
  each field's whole declaration as one precomputed string (`vendorExtensions.x-py-typing`), so
  a fork cannot drop one constraint. `pipeline/generate.sh` removes `max_length=N` from the
  model field annotations after generation, inside the pinned image, and fails generation if
  any survives anywhere in `models/`. Only `Annotated[str, Field(...)]` annotations are
  stripped, so a list bound would stop generation instead of being removed. 132 annotations in
  33 model files change and nothing else; `api/` keeps its 36 path and query parameter bounds.
- **Scope as built: model fields, in both directions.** PHP's deserializer calls the same
  setters, and Python's response models carry the same annotations, so a response with a longer
  value now binds instead of raising: a processed payment can no longer surface as a parse error
  over a length bound. Decision 2's "request body fields" reads "model fields".
- **A pattern that embeds a length kept refusing in SC-886.** As built in SC-886,
  `fraudPreventionPlatform`'s pattern `^[A-Za-z0-9._:-]{1,128}$` refused a 129-character value
  in Python and PHP, because decision 2 keeps patterns. The field is in `rtnData`, so since the
  amendment of 2026-11-26 (SC-1018) the Python and PHP cores send such a value as given. A
  pattern outside `rtnData` still refuses, for example `PaymentRequest.currency` (`^[A-Z]{3}$`).
- **Tests:** Python `tests/test_length_bounds.py` (six tests) and
  `test_merchant_transaction_id_over_100_is_left_to_the_platform`, which replaces the test that
  asserted the refusal; PHP `tests/LengthBoundsTest.php` (five tests). Against unmodified `main`
  the four Python and two PHP behaviour tests fail on the length refusal, and the tests for the
  kept checks pass. PHP's required-field evidence is the setter's non-null guard: a required
  field that is never set was not refused before this change either (nothing calls `valid()`),
  and the platform still answers it.
- **Decision 4's hold ends with this change:** Python 0.9.0 and PHP 0.10.0 release from it.

## Amendment — 2026-11-26 (SC-1018): Python and PHP do not refuse or rewrite `rtnData` values before sending

**Status:** Accepted — decided 2026-11-26 by Dimitri Pankov as RAP SDK author (SC-1018, closes
OQ-19). Implemented under SC-1018 (see [Implementation (SC-1018)](#implementation-sc-1018)
below); until the Python 0.11.2 and PHP 0.12.2 patch release, the published Python 0.11.1 and
PHP 0.12.1 keep the checks. No failover-contract change.

### Context

- Spec v2.20.0+92f2191 (Backbone PR #516, owner ruling by Charles Weiss on 2026-11-25), pinned
  in v2.21.0+66e302b, states that every `rtnData` field is an optional signal and that no
  `rtnData` value ever refuses the payment that carries it. The documented lengths, formats and
  value lists describe what the card issuers can use. A value outside them, or of the wrong JSON
  type, is accepted, and RTN trims, converts, shortens or leaves out that one value. Backbone
  removed every validation attribute from its ten `rtnData` models. `rtnData` appears only in
  `PaymentRequest` and `AuthorizeRequest`; no response schema carries it.
- Decision 2 kept the generated pattern, value-list, minimum and `minLength` checks. On the
  `rtnData` block the spec documents 10 patterns, 23 value lists, 20 minimums and 4 `minLength`
  bounds, plus 66 `maxLength` bounds that no SDK enforces since SC-886. The regenerated v2.21.0
  cores handle them as follows (measured on 2026-11-26: Python and PHP by running probes with
  synthetic values, the other four by reading the generated code):

  | Core | A value that breaks a pattern, minimum or `minLength` | A value outside a documented list |
  | --- | --- | --- |
  | Python | Refused on construction and on `from_dict` (`ValidationError`), so nothing is sent: 10 regular-expression validators, 20 `ge=` and 4 `min_length=` annotations in `models/rtn_data*.py` | Sent as given (the forked enum validator passes it through) |
  | PHP | Refused by the setter (`InvalidArgumentException`; 34 such checks in `lib/Model/RtnData*.php`); the array constructor checks nothing and sends it | The setter replaces it with `unknown_default_open_api` (`enumUnknownDefaultCase`); the array constructor sends it as given |
  | Java | Sent | `fromValue` maps an unlisted string to `UNKNOWN_DEFAULT_OPEN_API`, sent as `unknown_default_open_api`; `fromValue` is also the JSON creator, so a request read from JSON gets the sentinel too; the enum constants cannot express one |
  | .NET | Sent (`Validate` is never called) | Cannot be held by the closed enums: `FromString` throws `NotImplementedException`, and reading one from JSON throws `ArgumentNullException`, so nothing is sent |
  | TypeScript, Go | Sent | Sent as given |

- So a Python or PHP caller can still have a payment refused before sending over an `rtnData`
  value, which the platform no longer does. The PHP and Java replacement turns the caller's
  value into one RTN drops; it does not affect the payment. A .NET caller cannot build a
  request with an unlisted value, and one read from JSON is refused before sending.
- Types and formats are a separate matter. Each `rtnData` field has a JSON type (text, integer
  or boolean), and `orderData.purchaseDate` is a date-time. The spec accepts a value of the
  wrong JSON type, but the typed SDKs cannot express one, and Python's strict models refuse
  one read from a dictionary: for example, `"3"` for `orderData.itemCount`, or an unparseable
  `purchaseDate`. TypeScript's model also throws on serializing a `purchaseDate` that is not a
  date.
- Census (SC-1018 comment 28268; Backbone production telemetry, the 30 days to 2026-11-26
  19:00 UTC): no charge or authorize sent through an SDK carried `rtnData`; about 1,500 charges
  carrying `rtnData` came from four custom-integration accounts; the only outside account on the
  Python or PHP SDK is one PHP sandbox account, last seen on 2026-11-11. No merchant is affected
  today, so the change is preventive.
- `enumUnknownDefaultCase` exists for forward compatibility on responses (bake-off §A3) and stays
  as it is. `rtnData` is request-only, so passing an unlisted request value through does not
  touch that rule.

### Decision

1. **For the `rtnData` block, the Python and PHP SDKs neither refuse a request nor replace a
   value before sending** because the value breaks a documented pattern, value list, minimum
   or `minLength`. The platform's own rule decides, as decision 1 does for `maxLength`. The
   scope is `RtnData` and its ten nested models, the only schemas the platform exempts.
   Outside `rtnData`, decision 2 stands: patterns, value lists, ranges, `minLength`, required
   fields and non-null guards keep their generated checks. **Types and formats stay in every
   SDK:** a value must still have its field's type, and `purchaseDate` must still be a
   date-time, because the typed model is the SDK's interface; the platform's acceptance of a
   wrong JSON type serves callers who build the JSON themselves.
2. **Python: a generation step**, as SC-886 did. In `models/rtn_data*.py` only, it removes `ge=`
   and `min_length=` from the field annotations and removes the generated
   `_validate_regular_expression` validators. Generation fails if any of them survives in those
   files. The enum validators already pass values through and are untouched.
3. **PHP: a generation step or a template fork, scoped to the `RtnData*` models.** The stock
   template has no per-model switch, so the build chooses the mechanism under ADR-SDK-023. The
   setters stop throwing for a pattern, minimum or `minLength`, `listInvalidProperties()` drops
   those entries, and an unlisted value is stored as given instead of the sentinel. The
   non-null guards stay.
4. **Java and .NET: unchanged by this amendment, and recorded as kept.** Neither refuses a
   pattern, minimum or `minLength`. For an unlisted value, Java sends the sentinel (through
   `fromValue`, on construction and on the JSON path), and .NET cannot hold one and refuses
   one read from JSON. Opening their value lists means typing the 23 `rtnData` lists as plain
   strings, which changes public model types: a source-breaking change and a minor release.
   That is left for a separate decision if a merchant needs to send an unlisted value.
5. **Tests.** Each changed language gets tests proving that a value breaking each rule type is
   sent as given; they fail against today's cores. Two existing tests pin today's pattern
   refusal on `fraudPreventionPlatform` with the value `not allowed!` (Python
   `test_pattern_violation_is_still_refused` in `tests/test_length_bounds.py`, PHP
   `testPatternViolationIsStillRefused` in `tests/LengthBoundsTest.php`). They change with the
   revision, as `test_merchant_transaction_id_max_length_100` did in SC-886, and the kept
   pattern refusal moves to a field outside `rtnData` (`PaymentRequest.currency`,
   `^[A-Z]{3}$`, refused in both cores today), so a step that strips too much fails a test.
6. **Release.** Python and PHP are released as a patch: the SDK was stricter than the API it
   calls, which is a fix (`pipeline-and-release.md` §4). The other four packages are unchanged.
   The release notes state the handling rule neutrally.

### Consequences

- A Python or PHP caller's `rtnData` value of the right type reaches the platform as the caller
  built it, and RTN normalizes it, as already happens in TypeScript and Go.
- A caller loses the local error for a malformed signal. By its own contract the platform does
  not report one either, and RTN drops the value without telling anyone.
- Java and .NET keep typed value lists. A Java caller still sends the sentinel for an unlisted
  value, and a .NET request read from JSON with one is still refused before sending.
- No failover classification, error code or reconcile verdict changes. Outside `rtnData`, every
  generated check is as before.
- The implementation and the release are SC-1018 acceptance criteria 3 to 6.

### Implementation (SC-1018)

Implemented 2026-11-26 on PR #130 by two post-generation steps in `pipeline/generate.sh`, each
run inside the pinned image and selecting files by name: the `rtnData` family, `RtnData` and its
ten nested models, eleven files per language. The notes below on PHP types, PHP value lists,
future spec changes and the way back were ratified at Gate 2 on 2026-11-26 as the way the
decisions are carried out; they are implementation notes and do not change the decision text.

- **Python: a generation step after the SC-886 step.** In `models/rtn_data*.py` only, it
  removes 20 `ge=` and 4 `min_length=` annotations and 10 `_validate_regular_expression`
  validators. 7 of the 11 files change (24 lines added, 154 removed). It keeps the 94
  `strict=True` type checks, the `datetime` type of `orderData.purchaseDate` and the 23 enum
  validators. Generation fails if
  the file pattern matches no file, if a `ge=`, `gt=`, `min_length=` or regex validator
  survives, if the `strict=True` or enum validator count moves, or if the family's line count is
  not the old count less 13 for each removed validator.
- **Python: assignment and `from_dict` follow construction.** `validate_assignment` stays on, so
  a value assigned to a built model, or read by `from_dict`, meets the same rules as one given to
  the constructor: a wrong type is refused, and the removed rules are not applied.
- **PHP: a post-generation step, not a template fork.** The stock template has no per-model
  switch. The alternative, a second generator pass filtered to the family with its own template,
  produced byte-identical output but had three ways to fail that still finish without an error:
  the generated-code banner lost, the `maxLength` checks returning, or a mistyped list of model
  names writing one file. In `lib/Model/RtnData*.php` only, the step deletes whole lines and
  inserts none: 34 setter checks (10 pattern, 4 `minLength`, 20 minimum), 23 sentinel coercions
  (the setter replacing an unlisted value with `unknown_default_open_api`), and the matching 34
  rule entries and 23 value-list entries in `listInvalidProperties()`. 8 of the 11 files change
  (537 lines removed, none added). It keeps the 159 non-null guards, the 23
  `*_UNKNOWN_DEFAULT_OPEN_API` constants, the 23 `get*AllowableValues()` methods, `valid()` and
  `listInvalidProperties()`. Generation fails if the file pattern matches no file, if a removed
  check survives, if the non-null guard, constant or getter count moves, or if the family's line
  count is not the old count less the lines of the removed checks.
- **Nothing outside the family changed.** 15 generated files differ from `45e360c` in all
  (7 Python, 8 PHP); the .NET, Java, TypeScript and Go cores are unchanged.
- **PHP types (decision 1, as carried out).** The PHP setters checked no parameter type before
  this change and check none after; Python keeps every type check. A few wrong-type values were
  refused in PHP only as a side effect of the removed checks: an array given to a `minLength`
  setter, a value whose string form breaks a digit-only pattern, and an integer replaced by the
  sentinel on a list of text values. They are now sent as given.
- **PHP value lists (decision 3, as carried out).** The value-list entries also leave
  `listInvalidProperties()`, so `valid()` no longer reports an unlisted `rtnData` value.
  `valid()` is public. Nothing in the SDK calls it; whether a merchant calls it is not known.
- **Future spec changes.** In Python, a new exclusive minimum (`gt=`) or a new list bound on an
  `rtnData` field (pydantic writes one as `min_length=`) stops generation until the step is
  extended. In PHP, an exclusive minimum is removed like any minimum. The risk that a future
  schema named like the family but not part of `rtnData` is matched is recorded in
  `pipeline/python/config.yaml` and `pipeline/php/config.yaml`.
- **Tests:** Python `tests/test_rtn_data_values.py` covers each rule type on construction,
  `from_dict`, assignment and authorize, and proves that a wrong type is still refused on
  construction, on assignment and in `PaymentRequest.from_dict`. PHP `tests/RtnDataValuesTest.php`
  covers each rule type and an unlisted value on charge and authorize, and proves that the
  family's `listInvalidProperties()` is empty for breaking and unlisted values. The two tests
  that pinned the `not allowed!` refusal (decision 5) are now
  `test_pattern_outside_rtn_data_is_still_refused` and `testPatternOutsideRtnDataIsStillRefused`
  and pin the kept refusal on `PaymentRequest.currency`. Log-capture tests in both languages
  prove that a malformed `fullPan` is sent as given but never appears in a log record, a
  structured log field or a trace event of an approved charge or authorize. Against the previous
  cores 14 Python and 11 PHP tests fail; with this change all 202 Python and 135 PHP tests pass.
- **Way back.** There is no runtime switch: the behaviour ships inside the package and changes
  only when a merchant upgrades. A bad release is fixed by a forward patch, made from a reviewed
  revert of the tests and both steps together and released through the pipeline. No yank is
  approved in advance.
- **Release:** Python 0.11.2 and PHP 0.12.2, a patch (decision 6), cut from `main` after PR #130
  merges.
