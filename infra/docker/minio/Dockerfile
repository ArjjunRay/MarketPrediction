FROM golang:1.24-alpine AS build

# Last archived MinIO Community Edition source commit. The project moved to a
# source-only distribution; pinning prevents an unreviewed dependency change.
ARG MINIO_COMMIT=7aac2a2c5b7c882e68c1ce017d8256be2feea27f
RUN CGO_ENABLED=0 GOBIN=/out go install github.com/minio/minio@${MINIO_COMMIT}

FROM alpine:3.22
RUN apk add --no-cache ca-certificates curl su-exec \
    && addgroup -S minio \
    && adduser -S -G minio minio \
    && mkdir -p /data \
    && chown minio:minio /data
COPY --from=build /out/minio /usr/local/bin/minio
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 0755 /usr/local/bin/docker-entrypoint.sh
VOLUME ["/data"]
EXPOSE 9000 9001
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["server", "/data", "--console-address", ":9001"]
