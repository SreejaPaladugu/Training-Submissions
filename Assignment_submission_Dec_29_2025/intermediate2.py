import asyncio
import random
from collections import defaultdict

async def producer(queue, n=20):
    for _ in range(n):
        event = {
            "user_id": random.choice(["u1", "u2", "u3"]),
            "action": random.choice(["click", "purchase"]),
            "value": random.randint(10, 100)
        }
        await queue.put(event)
        print("PRODUCED:", event)
        await asyncio.sleep(0.1)

async def consumer(queue):
    revenue = defaultdict(int)

    while True:
        event = await queue.get()

        if event["action"] == "purchase":
            revenue[event["user_id"]] += event["value"]
            print("UPDATED REVENUE:", dict(revenue))

        queue.task_done()

async def main():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.join()

    consumer_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
