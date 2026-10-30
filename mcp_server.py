"""MCP server for Sliding Window Stream Aggregator."""
import sys
import json
from client import SlidingWindowStreamAggregator

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "process_window",
                    "description": "Aggregate time-stamped stream events into a sliding window with watermark late-event dropping",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "events": {"type": "array"},
                            "window_size_seconds": {"type": "number", "default": 60.0},
                            "watermark_delay_seconds": {"type": "number", "default": 10.0},
                            "current_time": {"type": "number"}
                        },
                        "required": ["events"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "process_window":
            out = SlidingWindowStreamAggregator.process_window(
                args.get("events", []),
                float(args.get("window_size_seconds", 60.0)),
                float(args.get("watermark_delay_seconds", 10.0)),
                args.get("current_time")
            )
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
    return {"error": "Unsupported method or tool"}

if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
