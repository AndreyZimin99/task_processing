import asyncio
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

logger = logging.getLogger(__name__)


async def worker(queue, semaphore):
    while True:
        task = await queue.get()
        if not task:
            break
        async with semaphore:
            logger.info(f'Задача {task['task_id']} принята в работу.')
            await asyncio.sleep(task['duration'])
            logger.info(f'Задача {task['task_id']} завершена.')
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    for i in range(100):
        task = {
            'task_id': i,
            'duration': random.uniform(0.5, 2.0)
        }
        await queue.put(task)
    semaphore = asyncio.Semaphore(5)
    workers = [asyncio.create_task(worker(queue, semaphore)) for _ in range(5)]
    await queue.join()
    for _ in workers:
        await queue.put(None)
    await asyncio.gather(*workers)


if __name__ == '__main__':
    asyncio.run(main())
