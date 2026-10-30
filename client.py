"""Sliding Window Stream Aggregator & Watermark Evictor.
100% Python Standard Library.
"""

import time

class SlidingWindowStreamAggregator:
    """Aggregates real-time agent telemetry events across sliding time windows with watermark eviction."""

    @staticmethod
    def process_window(events: list, window_size_seconds: float = 60.0,
                       watermark_delay_seconds: float = 10.0, current_time: float = None) -> dict:
        now = current_time if current_time is not None else time.time()
        watermark = now - watermark_delay_seconds
        window_start = now - window_size_seconds

        active_events = []
        dropped_late_events = []
        durations = []

        for e in events:
            event_ts = float(e.get("timestamp", now))
            if event_ts < watermark - window_size_seconds:
                dropped_late_events.append(e.get("event_id"))
            elif event_ts >= window_start:
                active_events.append(e)
                if "latency_ms" in e:
                    durations.append(float(e["latency_ms"]))

        durations.sort()
        avg_latency = (sum(durations) / len(durations)) if durations else 0.0
        p95_latency = durations[int(len(durations) * 0.95)] if durations else 0.0

        return {
            "window_start": round(window_start, 2),
            "window_end": round(now, 2),
            "watermark": round(watermark, 2),
            "active_events_count": len(active_events),
            "dropped_late_events_count": len(dropped_late_events),
            "metrics": {
                "avg_latency_ms": round(avg_latency, 2),
                "p95_latency_ms": round(p95_latency, 2),
                "throughput_events_per_sec": round(len(active_events) / max(1.0, window_size_seconds), 2)
            }
        }
