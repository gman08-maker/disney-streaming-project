import json
import random
import time
import uuid
from datetime import datetime, timezone

TITLES = ["Moana 2", "Andor", "Bluey", "The Bear", "Loki", "Encanto"]
EVENT_TYPES = ["play", "pause", "stop", "complete"]
DEVICES = ["tv", "phone", "web", "tablet"]


def make_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 5000)}",
        "title": random.choices(TITLES, weights=[5, 3, 4, 3, 2, 1])[0],
        "event_type": random.choices(EVENT_TYPES, weights=[6, 3, 3, 1])[0],
        "device": random.choice(DEVICES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    while True:
        print(json.dumps(make_event()), flush=True)
        time.sleep(random.uniform(0.05, 0.3))
