#!/bin/sh
set -eu

# Named volumes can retain ownership from an earlier image. Normalize it before
# dropping privileges so upgrades do not require deleting research artifacts.
chown -R minio:minio /data
exec su-exec minio minio "$@"

