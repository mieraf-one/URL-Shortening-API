from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import user as user_model, urls as urls_model
from app.utils import utils
from app.utils.url_generator import url_gen
from app.schemas import urls as urls_schema

from typing import List


router = APIRouter(
    tags=['URLs']
)

# -------------------------------------------------
#                   POST - URL
# -------------------------------------------------

@router.post('/', response_model=urls_schema.URLOutput)
def create_url(
        data: urls_schema.URLInput,
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    url_data = data.model_dump(exclude_unset=True)
    new_url = url_gen(data=url_data, owner_id=current_user.id, db=db)
    
    return new_url

# -------------------------------------------------
#                   GET - URL
# -------------------------------------------------

@router.get('/{shorten_url}')
def get_url(
        shorten_url: str,
        db: Session = Depends(get_db)
    ):
    
    # fetch url and check the owner
    url = (
        db.query(urls_model.URL)
            .filter(
                urls_model.URL.shorten_url == shorten_url)
            .first()
        )
    
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='url not found'
        )
    
    # increase click counts
    setattr(url, 'click_count', url.click_count + 1)
    db.commit()
    
    return RedirectResponse(url.original_url)


# -------------------------------------------------
#                   GET ALL - URL
# -------------------------------------------------

@router.get('/', response_model=List[urls_schema.URLOutput])
def create_url(
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    
    url = (
        db.query(urls_model.URL)
            .filter(
                urls_model.URL.owner_id == current_user.id)
            .all()
    )
    
    return url