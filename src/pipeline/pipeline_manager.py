import csv
import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional

from sqlalchemy.orm import Session

from src.core.logger import logger
from src.pipeline.ingestion import ingest_papers
from src.pipeline.processing import process_papers
from src.storage.crud import upsert_paper
from src.storage.db import SessionLocal
from src.api.cache import set_cache

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
CSV_PATH = os.path.join(OUTPUT_DIR, "papers.csv")
JSON_PATH = os.path.join(OUTPUT_DIR, "papers.json")


def _write_outputs(raw_papers, processed) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link", "authors", "abstract"])
        writer.writeheader()
        writer.writerows(raw_papers)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=4)


async def run_pipeline(
    db: Optional[Session] = None,
    limit: int = 5,
    skip: int = 0,
    write_outputs: bool = True,
) -> Dict:
    started = datetime.now(timezone.utc)
    owns_session = db is None
    db = db or SessionLocal()

    try:
        raw_papers = await ingest_papers(limit=limit, skip=skip)
        if not raw_papers:
            logger.warning("Pipeline: no papers ingested, skipping the rest of the run")
            return {"fetched": 0, "processed": 0, "stored": 0, "duration_seconds": 0}

        processed = process_papers(raw_papers)

        stored = 0
        for raw, structured in zip(raw_papers, processed):
            upsert_paper(db, structured, raw)
            stored += 1

        if write_outputs:
            _write_outputs(raw_papers, processed)

        set_cache(processed)

        duration = (datetime.now(timezone.utc) - started).total_seconds()
        summary = {
            "fetched": len(raw_papers),
            "processed": len(processed),
            "stored": stored,
            "duration_seconds": round(duration, 2),
        }
        logger.info(f"Pipeline: run complete — {summary}")
        return summary
    finally:
        if owns_session:
            db.close()