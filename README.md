# Disney Streaming Analytics Pipeline

Pipeline that computes trending films over a sliding window and processes simulated streaming occurences.

## Architecture
Generator -> Processor (sliding window) -> Console leaderboard

## Running Code
    python generator.py | python processor.py

## Test
    pytest

## Design notes
- Sliding window uses a deque plus a Counter. Each event is added and
  removed once (constant work/event).
- Uses event timestamps for efficient testing.
- Limitation: Events are in an assumed time order.
