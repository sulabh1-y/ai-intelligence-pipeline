from typing import Dict, List

from src.llm_engine.orchestrator import LLMOrchestrator
from src.core.logger import logger


def process_papers(raw_papers: List[Dict]) -> List[Dict]:
    llm = LLMOrchestrator()
    processed = []

    for paper in raw_papers:
        try:
            processed.append(llm.process_paper(paper))
        except Exception:
            logger.exception(f"Processing: failed to process paper {paper.get('link')}")

    logger.info(f"Processing: structured {len(processed)}/{len(raw_papers)} papers")
    return processed