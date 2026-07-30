# Security Policy

The RAP SDKs are payment-path client libraries. We take reports against them — and against
the RAP-core platform they talk to — seriously.

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues, discussions,
or pull requests.**

Use either private channel:

- Email **security@revaly.co**, or
- GitHub's private vulnerability reporting (**Security → Report a vulnerability** on this
  repository) — both reach the same team.

Include:

- the affected SDK language(s) and version(s) (or `api.revaly.co` for platform-side reports),
- a description of the issue and its impact,
- reproduction steps or a proof of concept, if available.

We will acknowledge your report promptly, keep you informed of progress, and credit you in
the fix's release notes if you wish. We ask for a reasonable coordinated-disclosure window
to remediate before any public write-up.

## Supported versions

The SDKs are pre-1.0. Security fixes land on the **latest released version** of each
language SDK; older pre-1.0 releases are not patched — upgrade to the newest release.
At GA this widens to **current + previous minor**, per the SDK's DX contract (§e).

| Version | Supported |
| --- | --- |
| Latest release per language | ✅ |
| Older pre-1.0 releases | ❌ (upgrade) |

## Scope

- The six SDKs in this repository (`languages/*`): .NET, Java, PHP, TypeScript, Python, Go.
- Vulnerabilities in the RAP-core service behind `api.revaly.co` — same intake, same address.

## A note on sensitive data

SDK logs are values-free by design: no payload values at default verbosity, and API keys
never appear in logs or exception messages. If you believe you have found a path where card
data, credentials, or merchant payload values can leak into logs, exceptions, or telemetry,
that is in scope — report it. Never post card numbers, CVVs, or live API keys in any public
channel while doing so.
