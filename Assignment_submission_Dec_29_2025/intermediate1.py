import time
from collections import defaultdict

# Real-ish dataset (could come from logs, app events, etc.)
events = [
    {"user_id": "u1", "action": "view", "value": 0},
    {"user_id": "u2", "action": "click", "value": 0},
    {"user_id": "u1", "action": "click", "value": 0},
    {"user_id": "u3", "action": "purchase", "value": 40},
    {"user_id": "u2", "action": "purchase", "value": 25},
    {"user_id": "u1", "action": "purchase", "value": 100},
    {"user_id": "u2", "action": "click", "value": 0},
]

clicks = defaultdict(int)
purchases = defaultdict(int)
revenue = defaultdict(int)

print("Streaming events...\n")

for e in events:
    # stream comes event by event
    time.sleep(0.2)

    if e["action"] == "click":
        clicks[e["user_id"]] += 1

    if e["action"] == "purchase":
        purchases[e["user_id"]] += 1
        revenue[e["user_id"]] += e["value"]

    print("EVENT:", e)

print("\n--- RESULTS ---")
print("Clicks per user:", dict(clicks))
print("Purchases per user:", dict(purchases))
print("Revenue per user:", dict(revenue))
