import asyncio
import random
from collections import defaultdict

BATCH_SIZE = 50

async def producer(queue, n=1000):
    for _ in range(n):
        await queue.put({
            "user_id": random.choice(["u1", "u2", "u3"]),
            "action": random.choice(["click", "purchase"]),
            "value": random.randint(10, 100)
        })
    await queue.put(None)  # stop signal

async def consumer(queue):
    revenue = defaultdict(int)
    batch = []

    while True:
        event = await queue.get()
        if event is None:
            break

        batch.append(event)

        if len(batch) >= BATCH_SIZE:
            for e in batch:
                if e["action"] == "purchase":
                    revenue[e["user_id"]] += e["value"]
            batch.clear()

    # process leftover events
    for e in batch:
        if e["action"] == "purchase":
            revenue[e["user_id"]] += e["value"]

    print("FINAL REVENUE:", dict(revenue))

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

if __name__ == "__main__":
    asyncio.run(main())
