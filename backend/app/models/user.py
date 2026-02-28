from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.utils.database import Base
from app.models import urls as urls_model


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name= Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True, name='email')
    username = Column(String, unique=True, nullable=False, name='username', index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    urls = relationship(
        'URL',
        back_populates='owner'
    )
