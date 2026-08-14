import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import asyncio
from src.crawler.base import BaseCrawler

async def main():
    crawler = BaseCrawler()

    url = "https://example.com"
    data = await crawler.fetch(url)

    if data:
        print("Data fetched successfully!")
        print(data[:500])  # print first 500 characters

if __name__ == "__main__":
    asyncio.run(main())