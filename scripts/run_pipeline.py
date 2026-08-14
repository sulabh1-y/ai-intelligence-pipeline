import asyncio
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.core.logger import logger  # noqa: E402
from src.storage.db import init_db  # noqa: E402
from src.pipeline.pipeline_manager import run_pipeline  # noqa: E402


async def main():
    init_db()
    summary = await run_pipeline()
    logger.info(f"run_pipeline: {summary}")
    print(summary)


if __name__ == "__main__":
    asyncio.run(main())