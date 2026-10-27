# Security foundation

- No secrets belong in source control or `NEXT_PUBLIC_*` variables.
- Provider credentials remain server-side.
- CORS defaults to local development origins and must be explicit in production.
- Public capabilities are policy-controlled from verified source rights.
- Logs must not contain credentials, authorization headers, or raw private news content.
- Production requires TLS, rate limiting, secret management, and dependency/container scanning.

The main application is anonymous. No authentication, registration, OAuth provider, or
private dashboard is in the current roadmap. Operator-side provider configuration stays
server-only.
