# Deployment

The system is containerized and portable; AWS is the preferred future target but no
cloud resources are provisioned. A production design may map the API/processors to a
container service, PostgreSQL to RDS-compatible storage, Redis to a managed cache,
Redpanda/Kafka to a managed stream, and object artifacts to S3.

Terraform remains an empty boundary until cloud, region, availability, traffic,
retention, provider egress, and budget decisions are approved. Production also needs
TLS/domain configuration, a secrets manager, backups and restore tests, rate limiting,
WAF/edge policy, tracing, alerts, and anonymous-public rate limiting.

There is no GitHub integration, remote, workflow, or deployment automation.
