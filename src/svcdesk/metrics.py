# ai-generated: 95% - AI implemented a small Prometheus histogram and ASGI instrumentation.
"""Request-duration histogram with stable route labels and Prometheus text output."""

from __future__ import annotations

import bisect
import threading
import time
from collections import defaultdict
from typing import Any


# Fine resolution around the measured p99 (~0.131 s), with broad coverage outside it.
BUCKETS: tuple[float, ...] = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.115,
    0.12,
    0.125,
    0.13,
    0.135,
    0.14,
    0.145,
    0.15,
    0.2,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
)
METRIC_NAME = "http_server_request_duration_seconds"


class RequestHistogram:
    def __init__(self, buckets: tuple[float, ...] = BUCKETS) -> None:
        if tuple(sorted(set(buckets))) != buckets or any(value <= 0 for value in buckets):
            raise ValueError("histogram buckets must be strictly increasing and positive")
        if len(buckets) > 30:
            raise ValueError("at most 30 finite histogram buckets are allowed")
        self.buckets = buckets
        self._lock = threading.Lock()
        self._counts: dict[tuple[str, str, str], list[int]] = defaultdict(lambda: [0] * (len(buckets) + 1))
        self._sums: dict[tuple[str, str, str], float] = defaultdict(float)

    def observe(self, method: str, route: str, status: int, seconds: float) -> None:
        labels = (method, route, str(status))
        bucket_index = bisect.bisect_left(self.buckets, seconds)
        with self._lock:
            self._counts[labels][bucket_index] += 1
            self._sums[labels] += seconds

    def exposition(self) -> str:
        lines = [
            f"# HELP {METRIC_NAME} Duration of HTTP server requests in seconds.",
            f"# TYPE {METRIC_NAME} histogram",
        ]
        with self._lock:
            rows = [(labels, counts.copy(), self._sums[labels]) for labels, counts in self._counts.items()]
        for labels, counts, total in sorted(rows):
            method, route, status = labels
            rendered = (
                f'http_request_method="{method}",http_route="{route}",'
                f'http_response_status_code="{status}"'
            )
            cumulative = 0
            for index, boundary in enumerate(self.buckets):
                cumulative += counts[index]
                lines.append(
                    f'{METRIC_NAME}_bucket{{{rendered},le="{boundary:g}"}} {cumulative}'
                )
            count = sum(counts)
            lines.append(f'{METRIC_NAME}_bucket{{{rendered},le="+Inf"}} {count}')
            lines.append(f"{METRIC_NAME}_sum{{{rendered}}} {total:.12g}")
            lines.append(f"{METRIC_NAME}_count{{{rendered}}} {count}")
        return "\n".join(lines) + "\n"


HISTOGRAM = RequestHistogram()


class RequestMetricsMiddleware:
    """Observe each completed HTTP response once, using its matched route template."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http" or scope.get("path") == "/metrics":
            await self.app(scope, receive, send)
            return

        started = time.perf_counter()
        status = 500

        async def send_with_status(message: dict[str, Any]) -> None:
            nonlocal status
            if message.get("type") == "http.response.start":
                status = int(message.get("status", 500))
            await send(message)

        try:
            await self.app(scope, receive, send_with_status)
        finally:
            route = scope.get("route")
            route_template = getattr(route, "path", None) or "unmatched"
            HISTOGRAM.observe(
                str(scope.get("method", "GET")),
                str(route_template),
                status,
                time.perf_counter() - started,
            )
