from typing import List, Optional

from sqlalchemy.orm import Session

from src.storage.models import Paper


def get_paper_by_link(db: Session, link: str) -> Optional[Paper]:
    return db.query(Paper).filter(Paper.link == link).first()


def upsert_paper(db: Session, structured: dict, raw: dict) -> Paper:
    existing = get_paper_by_link(db, raw["link"])
    if existing:
        return existing

    content = structured["content"]
    authors = content["authors"]
    if isinstance(authors, list):
        authors = ", ".join(authors)

    paper = Paper(
        title=content["title"],
        link=raw["link"],
        authors=authors,
        abstract=raw.get("abstract"),
        category=content["category"],
        summary=content["summary"],
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


def list_papers(db: Session, limit: int = 20, category: Optional[str] = None) -> List[Paper]:
    query = db.query(Paper).order_by(Paper.created_at.desc())
    if category:
        query = query.filter(Paper.category.ilike(category))
    return query.limit(limit).all()


def count_papers(db: Session) -> int:
    return db.query(Paper).count()