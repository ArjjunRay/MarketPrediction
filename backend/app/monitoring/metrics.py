from prometheus_client import Counter, Gauge, Histogram

HTTP_REQUESTS = Counter(
    "qstream_http_requests_total", "HTTP requests", ("method", "path", "status")
)
HTTP_LATENCY = Histogram(
    "qstream_http_request_duration_seconds", "HTTP request latency", ("method", "path")
)
WEBSOCKET_CONNECTIONS = Gauge(
    "qstream_websocket_connections", "Currently connected market WebSockets"
)
