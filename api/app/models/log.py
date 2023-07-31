from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
from datetime import datetime

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True )
    data = Column(String)
    data_hash = Column(String)
    match_with_ground_truth = Column(Boolean)
    ground_truth_id = Column(Integer, nullable=True)
    suggestion = Column(String, nullable=True)
    updated_by = Column(Integer, nullable=True)
    valid_from = Column(DateTime(timezone=True), nullable=True)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
