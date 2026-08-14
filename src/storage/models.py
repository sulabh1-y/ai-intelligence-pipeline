from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from src.storage.db import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False, index=True)
    authors = Column(Text, nullable=True)
    abstract = Column(Text, nullable=True)
    category = Column(String, nullable=True, index=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())