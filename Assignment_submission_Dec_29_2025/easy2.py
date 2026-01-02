import time
import random
from collections import deque

# A "topic" (Kafka-like) simulated by a queue
topic = deque()

def producer(topic, n=10):
    """Produces events and pushes them to the topic."""
    for i in range(n):
        event = {
            "event_id": i,
            "user_id": random.choice(["u1", "u2", "u3"]),
            "action": random.choice(["click", "view", "purchase"]),
            "value": random.randint(1, 100),
            "ts": time.time()
        }
        topic.append(event)
        print(f"PRODUCED: {event}")
        time.sleep(0.3)

def consumer(topic):
    """Consumes events and processes them."""
    while topic:
        event = topic.popleft()
        # Example processing: filter only purchases
        if event["action"] == "purchase":
            print(f"CONSUMED (purchase): user={event['user_id']} value={event['value']}")
        else:
            print(f"CONSUMED (ignored): action={event['action']}")

if __name__ == "__main__":
    producer(topic, n=12)
    print("\n--- START CONSUMER ---\n")
    consumer(topic)
