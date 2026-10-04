"""Reads JSON events from stdin and prints the top titles in the last 5 minutes.

Run it with the generator piped in:
    python generator.py | python processor.py
"""
import json
import sys
from datetime import datetime

from window import SlidingWindowCounter

WINDOW_SECONDS = 300      # 5 minutes
PRINT_EVERY_SECONDS = 1   # how often (in event time) to print the leaderboard


def parse_event(line):
    """Return (event_dict, unix_timestamp), or None if the line is malformed."""
    try:
        event = json.loads(line)
        timestamp = datetime.fromisoformat(event["timestamp"]).timestamp()
        event["title"], event["event_type"]  # make sure these keys exist
        return event, timestamp
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return None


def main():
    counter = SlidingWindowCounter(WINDOW_SECONDS)
    last_print = None
    malformed = 0

    for line in sys.stdin:
        parsed = parse_event(line)
        if parsed is None:
            malformed += 1
            continue

        event, ts = parsed
        if event["event_type"] == "play":
            counter.add(event["title"], ts)

        if last_print is None or ts - last_print >= PRINT_EVERY_SECONDS:
            last_print = ts
            top = counter.top(5, now=ts)
            summary = ", ".join(f"{title}: {n}" for title, n in top)
            print(f"[plays, last 5 min] {summary}  (malformed skipped: {malformed})",
                  flush=True)


if __name__ == "__main__":
    main()