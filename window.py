from collections import Counter, deque


class SlidingWindowCounter:
    """Counts how many times each key was seen in the last `window_seconds`.

    An event with timestamp t is counted while  now - window_seconds < t <= now.
    Timestamps are plain numbers (seconds), and events are expected to arrive in
    roughly increasing time order.
    """

    def __init__(self, window_seconds=300):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self.window_seconds = window_seconds
        self._events = deque()   # (timestamp, key), oldest on the left
        self._counts = Counter()  # key -> count inside the current window

    def add(self, key, timestamp):
        """Record one event, then drop anything that fell out of the window."""
        self._events.append((timestamp, key))
        self._counts[key] += 1
        self._evict(timestamp)

    def count(self, key, now):
        """How many times `key` appeared in the window ending at `now`."""
        self._evict(now)
        return self._counts.get(key, 0)

    def top(self, n, now):
        """The n most frequent keys in the window ending at `now`."""
        self._evict(now)
        return self._counts.most_common(n)

    def _evict(self, now):
        cutoff = now - self.window_seconds
        while self._events and self._events[0][0] <= cutoff:
            _, key = self._events.popleft()
            self._counts[key] -= 1
            if self._counts[key] == 0:
                del self._counts[key]