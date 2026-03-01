from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import user as user_model, urls as urls_model
from app.utils import utils
from app.schemas import urls as urls_schema


router = APIRouter(
    tags=['URLs'],
    prefix='/urls'
)


@router.post('', response_model=urls_schema.URLOutput)
def create_url(
        data: urls_schema.URLInput,
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    url_data = data.model_dump(exclude_unset=True)
    url_data['owner'] = current_user
    
    gen_url = '/elyas'
    if not url_data.get('shorten_url'):
        url_data['shorten_url'] = gen_url
        
    new_url = urls_model.URL(**url_data)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    
    return new_url