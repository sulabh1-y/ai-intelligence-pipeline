from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaperBase(BaseModel):
    title: str
    link: str
    authors: str
    abstract: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperOut(PaperBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True