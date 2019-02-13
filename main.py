import asyncio
import time
from client.master import Client104


async def run_client():
    client = Client104()
    client.start()
    await asyncio.sleep(10)


async def run_writer():


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    # task1 = asyncio.create_task(say_after(1.2, 'hello'))
    # task2 = asyncio.create_task(say_after(1.1, 'world'))
    # print(f"started at {time.strftime('%X')}")
    task_client = asyncio.create_task(run_client())
    await task_client

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
