from pydantic import BaseModel
from datetime import datetime

class OwnerOut(BaseModel):
    id: str
    username: str
        
class URLInput(BaseModel):
    original_url: str
    shorten_url: str | None = None

class URLOutput(BaseModel):
    id: int
    owner_id: int
    original_url: str
    shorten_url: str
    click_count: int
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True