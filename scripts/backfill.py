import argparse
import asyncio
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.core.logger import logger  # noqa: E402
from src.storage.db import init_db  # noqa: E402
from src.pipeline.pipeline_manager import run_pipeline  # noqa: E402


async def backfill(pages: int, page_size: int, delay_seconds: float) -> None:
    init_db()
    total_stored = 0

    for page in range(pages):
        skip = page * page_size
        logger.info(f"Backfill: page {page + 1}/{pages} (skip={skip})")

        summary = await run_pipeline(
            limit=page_size, skip=skip, write_outputs=(page == pages - 1)
        )
        total_stored += summary["stored"]

        if summary["fetched"] == 0:
            logger.info("Backfill: no more papers returned, stopping early")
            break

        await asyncio.sleep(delay_seconds)

    logger.info(f"Backfill: complete — {total_stored} papers stored across {pages} page(s)")
    print(f"Backfill complete: {total_stored} papers stored")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill older papers into the database.")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to walk back (default: 5)")
    parser.add_argument("--page-size", type=int, default=5, help="Papers per page (default: 5)")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between pages (default: 2.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asyncio.run(backfill(args.pages, args.page_size, args.delay))


if __name__ == "__main__":
    main()