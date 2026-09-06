# SAP Concur Connector — Auth & Credentials Standard (B1–B10)

## B1: Credential Storage
Credentials are stored securely in Imperal Secrets vault under `sap_concur_connections`. Raw tokens are never returned across user-facing tools or chat completions.

## B2: Masking & Presentation
Tokens are masked showing only leading/trailing characters (`ab12…ef34`) or generic redaction `***`.

## B3: Authentication Verification
Verification executes a non-destructive identity check (`GET /profile/identity/v4/Users/me`) during connection onboarding before persisting credentials.

## B7: Regional Architecture
Default endpoint is `https://us.api.concursolutions.com`, with support for custom datacenter regional URLs (EMEA/APAC) via `base_url`.

## B8 & B10: Error Classification & Sanitization
All client methods classify HTTP 429 (`RATE_LIMITED` + `Retry-After`), HTTP 401 (`UNAUTHORIZED`), and HTTP 403 (`FORBIDDEN`). Errors sanitize tokens to prevent credential leaks.

## B9: Multi-Tenant Isolation
All data operations require or resolve an explicit `connection_id`, ensuring strict tenant isolation.
