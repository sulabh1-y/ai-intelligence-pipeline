import argparse
import asyncio
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.core.logger import logger  # noqa: E402
from src.storage.db import init_db  # noqa: E402
from src.pipeline.pipeline_manager import run_pipeline  # noqa: E402

DEFAULT_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "60"))


async def run_forever(interval_minutes: int) -> None:
    interval_seconds = max(interval_minutes, 1) * 60
    logger.info(f"Scheduler: running every {interval_minutes} minute(s)")

    while True:
        await run_pipeline()
        logger.info(f"Scheduler: sleeping for {interval_minutes} minute(s)")
        await asyncio.sleep(interval_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the papers pipeline on a schedule.")
    parser.add_argument("--once", action="store_true", help="Run a single pass and exit.")
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_MINUTES,
        help=f"Minutes between runs (default: {DEFAULT_INTERVAL_MINUTES}, or SCRAPE_INTERVAL_MINUTES env var).",
    )
    return parser.parse_args()


def main() -> None:
    init_db()
    args = parse_args()

    try:
        if args.once:
            asyncio.run(run_pipeline())
        else:
            asyncio.run(run_forever(args.interval))
    except KeyboardInterrupt:
        logger.info("Scheduler: stopped by user")


if __name__ == "__main__":
    main()