from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.database.session import Base

if TYPE_CHECKING:
    from .note import Note


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True))
    modified_at = Column(DateTime(timezone=True))

    notes = relationship("Note", back_populates="author_id")
