from typing import Dict, List

from src.crawler.papers_scraper import PapersScraper
from src.core.logger import logger


async def ingest_papers(limit: int = 5, skip: int = 0) -> List[Dict]:
    scraper = PapersScraper()
    papers = await scraper.scrape_papers(limit=limit, skip=skip)
    logger.info(f"Ingestion: fetched {len(papers)} raw papers (skip={skip})")
    return papers