"""Example usage for Sliding Window Stream Aggregator."""
from client import SlidingWindowStreamAggregator

if __name__ == "__main__":
    events = [
        {"event_id": "req-1", "timestamp": 100.0, "latency_ms": 45.0},
        {"event_id": "req-2", "timestamp": 120.0, "latency_ms": 65.0}
    ]
    res = SlidingWindowStreamAggregator.process_window(events, window_size_seconds=60.0, current_time=130.0)
    print("Aggregated Window:", res)
