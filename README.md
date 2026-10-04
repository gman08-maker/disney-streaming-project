# Disney Streaming Analytics Pipeline

A real-time pipeline that processes simulated streaming-viewing events and
computes trending titles over a 5-minute sliding window.

## Architecture
Generator -> Processor (sliding window) -> console leaderboard

## Run it
    python generator.py | python processor.py

## Tests
    pytest

## Design notes
- Sliding window uses a deque plus a Counter, so each event is added and
  removed once (constant work per event).
- Uses event timestamps rather than the system clock, so it is easy to test.
- Known limitation: assumes events arrive in time order.
