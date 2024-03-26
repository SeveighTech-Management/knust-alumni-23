from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Graduates(Base):
    __tablename__ = "graduates"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    graduate_name = Column("graduate_name", String(2004))
    graduate_year = Column("graduate_year", String(2004))
    picture_name = Column("picture_name", String(2004))
    comment = relationship("Comments", back_populates="graduate_info")


class Comments(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    comment = Column("comment", String(2004))
    name_of_commenter = Column("name_of_commenter", String(2004))
    graduate_id = Column(UUID(as_uuid=True), ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="comment")
