import time
import random
from collections import defaultdict, deque

topic = deque()

STATUSES = ["applied", "screening", "interview", "offer", "rejected"]
COMPANIES = ["BCBS", "Amazon", "Google", "Walmart", "Techfinity"]

def producer(topic, n=30):
    for i in range(n):
        event = {
            "event_id": i,
            "company": random.choice(COMPANIES),
            "status": random.choice(STATUSES),
            "ts": time.time()
        }
        topic.append(event)
        time.sleep(0.1)

def consumer(topic):
    status_counts = defaultdict(int)
    company_counts = defaultdict(int)

    while topic:
        event = topic.popleft()

        status_counts[event["status"]] += 1
        company_counts[event["company"]] += 1

        # print live dashboard
        print("\nEVENT:", event)
        print("STATUS COUNTS:", dict(status_counts))
        print("TOP COMPANIES:", dict(company_counts))

if __name__ == "__main__":
    producer(topic)
    consumer(topic)
