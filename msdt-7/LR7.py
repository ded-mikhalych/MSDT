import asyncio
import aiohttp
import logging
import json
from aiohttp import ClientSession, ClientTimeout
from tqdm import tqdm
from typing import List
from aiofiles import open as aio_open

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Таймаут для HTTP-запросов
TIMEOUT = 10

# Ограничение на количество одновременных запросов
CONCURRENT_REQUESTS = 5

async def fetch(session: ClientSession, url: str) -> dict:
    """Асинхронно получает данные по указанному URL."""
    try:
        async with session.get(url, timeout=ClientTimeout(total=TIMEOUT)) as response:
            content = await response.text()
            return {"url": url, "status": response.status, "content": content[:500]}  # Ограничиваем длину для демонстрации
    except Exception as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return {"url": url, "status": "error", "content": str(e)}

async def worker(name: str, session: ClientSession, queue: asyncio.Queue, results: List[dict]):
    """Работник, который обрабатывает задачи из очереди."""
    while True:
        url = await queue.get()
        logger.info(f"Worker {name} is fetching: {url}")
        result = await fetch(session, url)
        results.append(result)
        queue.task_done()

async def scrape_websites(urls: List[str], num_workers: int = CONCURRENT_REQUESTS):
    """Асинхронно обрабатывает несколько запросов к веб-сайтам с использованием пула воркеров."""
    queue = asyncio.Queue()
    results = []

    for url in urls:
        queue.put_nowait(url)

    async with ClientSession() as session:
        workers = [asyncio.create_task(worker(f"Worker-{i+1}", session, queue, results)) for i in range(num_workers)]
        await queue.join()

        for w in workers:
            w.cancel()

    return results

async def save_results_to_file(results: List[dict], filename: str):
    """Асинхронно сохраняет результаты в JSON-файл."""
    async with aio_open(filename, 'w') as f:
        await f.write(json.dumps(results, indent=4))

async def main(urls: List[str], output_file: str, num_workers: int):
    logger.info("Starting the scraping process...")
    results = await scrape_websites(urls, num_workers)

    logger.info(f"Saving results to {output_file}")
    await save_results_to_file(results, output_file)

    logger.info("Scraping completed successfully!")

async def run_main():  # Создаем асинхронную функцию для запуска main
    # Список URL для скрейпинга
    urls = [
        "https://www.kuklosknights.com/",
        "https://feor.ru/",
        "https://www.jewrf.ru/",
        "https://nasiliu.net/",
        "https://aasamara.ru/",
        "https://jesus-portal.ru/",
        "https://jesusischrist.ru/",
        "https://www.cygane.info/",
        "https://сапёр.com/",
        "https://www.mossad.gov.il/eng/Pages/default.aspx",
        "https://www.drive2.ru/",
        "https://www.python.org",
    ]
    output_file = "results.json"
    num_workers = 5
    await main(urls, output_file, num_workers)  # Вызываем main с помощью await

if __name__ == "__main__":
    await run_main()  # Запускаем асинхронную функцию
