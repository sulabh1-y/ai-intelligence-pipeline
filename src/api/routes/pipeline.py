from fastapi import APIRouter, Query
from typing import Optional

from src.crawler.papers_scraper import PapersScraper
from src.llm_engine.orchestrator import LLMOrchestrator
from src.api.cache import get_cache, set_cache

router = APIRouter()


@router.get("/papers")
async def get_papers(
    limit: int = Query(5, ge=1, le=20),
    category: Optional[str] = None
):
    # 🔥 STEP 1: Check cache
    cached_data = get_cache()

    if cached_data:
        print("⚡ Returning cached data")
        data = cached_data
    else:
        print("🐢 Fetching fresh data...")

        scraper = PapersScraper()
        papers = await scraper.scrape_papers()

        llm = LLMOrchestrator()

        data = []
        for p in papers:
            structured = llm.process_paper(p)
            data.append(structured)

        # 🔥 STEP 2: Store in cache
        set_cache(data)

    # 🔥 STEP 3: Apply filters
    filtered = []

    for item in data:
        if category:
            if item["content"]["category"].lower() != category.lower():
                continue

        filtered.append(item)

    return filtered[:limit]