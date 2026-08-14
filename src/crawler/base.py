import aiohttp
import asyncio
from src.core.logger import logger

class BaseCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    async def fetch(self, url):
        try:
            async with aiohttp.ClientSession() as session:
               async with session.get(url, headers=self.headers, ssl=False) as response:
                    if response.status == 200:
                        data = await response.text()
                        logger.info(f"Fetched: {url}")
                        return data
                    else:
                        logger.error(f"Failed {url} - Status: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None