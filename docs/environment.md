# Environment variables

Copy `.env.example` to `.env` for local overrides. Never commit `.env` or real credentials.

## Runtime

| Variable | Purpose | Local default |
| --- | --- | --- |
| `QSTREAM_ENV` | Runtime environment label used by application configuration and logs | `development` |
| `QSTREAM_LOG_LEVEL` | Backend structured-log severity | `INFO` |
| `QSTREAM_API_HOST` | API bind address inside its container | `0.0.0.0` |
| `QSTREAM_API_PORT` | API bind port inside its container | `8000` |
| `QSTREAM_PUBLIC_MODE` | Restricts runtime to publicly displayable capabilities | `true` |
| `QSTREAM_ALLOWED_ORIGINS` | JSON list of browser origins permitted by CORS | `["http://localhost:33000"]` |
| `QSTREAM_ENABLE_SIMULATED_PROVIDER` | Explicit opt-in to the labeled development-only feed | `false` |
| `QSTREAM_SEC_USER_AGENT` | Operator name and contact email required by SEC fair-access policy; not a browser-user credential | empty |
| `QSTREAM_BEA_API_KEY` | Free operator-owned key for BEA macro data; never requested from browser users | empty |
| `QSTREAM_PUBLIC_DATA_TIMEOUT_SECONDS` | Timeout for fixed-host SEC, BLS and Treasury requests | `30` |
| `NEXT_PUBLIC_API_URL` | Browser-visible HTTP API base URL | `http://localhost:38000` |
| `NEXT_PUBLIC_WS_URL` | Browser-visible WebSocket base URL | `ws://localhost:38000` |

## Storage and streaming

| Variable | Purpose | Local default |
| --- | --- | --- |
| `POSTGRES_DB` | PostgreSQL database name | `qstream` |
| `POSTGRES_USER` | PostgreSQL user | `qstream` |
| `POSTGRES_PASSWORD` | PostgreSQL password; replace outside disposable local use | local placeholder |
| `QSTREAM_DATABASE_URL` | Async SQLAlchemy database URL | Compose PostgreSQL service |
| `QSTREAM_REDIS_URL` | Redis live-state URL | Compose Redis service |
| `QSTREAM_KAFKA_BOOTSTRAP_SERVERS` | Kafka-compatible broker list | Compose Redpanda service |
| `QSTREAM_SCHEMA_REGISTRY_URL` | Redpanda Schema Registry URL | Compose Redpanda service |
| `MINIO_ROOT_USER` | Local MinIO administrator/access key | `qstream` |
| `MINIO_ROOT_PASSWORD` | Local MinIO administrator/secret key; replace locally | local placeholder |
| `QSTREAM_S3_ENDPOINT` | S3-compatible object-store endpoint | Compose MinIO service |
| `QSTREAM_S3_ACCESS_KEY` | S3-compatible access key | local MinIO user |
| `QSTREAM_S3_SECRET_KEY` | S3-compatible secret key | local MinIO password |
| `QSTREAM_S3_BUCKET` | Raw/research artifact bucket | `qstream-local` |
| `QSTREAM_S3_REGION` | S3 signing region | `us-east-1` |

## Host ports and optional observability

`QSTREAM_POSTGRES_PORT`, `QSTREAM_REDIS_PORT`, `QSTREAM_REDPANDA_KAFKA_PORT`,
`QSTREAM_REDPANDA_SCHEMA_PORT`, `QSTREAM_REDPANDA_ADMIN_PORT`,
`QSTREAM_MINIO_PORT`, `QSTREAM_MINIO_CONSOLE_PORT`, `QSTREAM_BACKEND_PORT`,
`QSTREAM_FRONTEND_PORT`, `QSTREAM_PROMETHEUS_PORT`, and
`QSTREAM_GRAFANA_PORT` control host-side Compose port mappings. Container-to-container
addresses do not change. `GRAFANA_ADMIN_PASSWORD` controls the optional local Grafana
administrator password and must be replaced before non-disposable use.

## Provider configuration

No paid-provider credential variables are defined. `QSTREAM_SEC_USER_AGENT` identifies
the backend operator to SEC and should contain an application/operator name plus contact
email. `QSTREAM_BEA_API_KEY` is obtained through BEA's free registration. Browser users
never configure a source or key. No server-only value may be exposed through
`NEXT_PUBLIC_*`.
