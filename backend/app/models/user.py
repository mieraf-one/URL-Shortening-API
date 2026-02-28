from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.utils.database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name= Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    urls = relationship(
        'URL',
        back_populates='owner'
    )
