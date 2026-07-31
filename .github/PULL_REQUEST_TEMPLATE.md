## What

<!-- One-paragraph summary. Title follows conventional commits, e.g. `feat(go): …`, `docs: …`. -->

## Checklist

- [ ] **No hand edits under `languages/*/core/`** — generated code changes only by
      regeneration against a newly pinned spec artifact (CI enforces the regeneration diff).
- [ ] **Values-free**: no payload values, card data, or API keys in log output, exception
      messages, tests, or fixtures — synthetic data only.
- [ ] Failure classification follows `docs/failover-contract.md`: status + `code` only,
      open strings, unknown → OutcomeUnknown; no retries, resubmission, or cross-request
      state introduced.
- [ ] Any example handling verdicts or error codes keeps the mandatory default/else branch.
- [ ] Tests added or updated in the affected language(s).
- [ ] Docs updated where behaviour changed (an ADR for decisions; README/quickstart for
      surface changes).
