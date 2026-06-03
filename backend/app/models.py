from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func

Base = declarative_base()


class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(3), nullable=False)
    clear_time_ms = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
