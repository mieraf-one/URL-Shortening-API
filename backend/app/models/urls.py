from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.utils.database import Base
from app.models import user as user_model


class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    original_url = Column(String, nullable=False)
    shorten_url = Column(String, nullable=False, index=True)
    click_count = Column(Integer, default=0)
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    owner = relationship(
        'User',
        back_populates='urls',
    )
