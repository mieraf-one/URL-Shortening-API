from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import user as user_model, urls as urls_model
from app.utils import utils
from app.utils.url_generator import url_gen
from app.schemas import urls as urls_schema

from typing import List
from datetime import datetime, timezone


router = APIRouter(
    tags=['URLs']
)

# -------------------------------------------------
#                   POST - URL
# -------------------------------------------------

@router.post('/', response_model=urls_schema.URLOutput)
def create_url(
        data: urls_schema.URLInput,
        request: Request,
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    url_data = data.model_dump(exclude_unset=True)
    new_url = url_gen(data=url_data, owner_id=current_user.id, db=db)
    
    # add domain to shorten url
    update_url = urls_schema.URLOutput.model_validate(new_url)
    update_url.shorten_url = f'{request.base_url}{new_url.shorten_url}'
    
    return update_url

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
                urls_model.URL.shorten_url == shorten_url,
                urls_model.URL.is_deleted != True)
            .first()
        )
    
    # check url existance
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='url not found'
        )
    
    # check expiration time
    if url.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='url expired'
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
        request: Request,
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    
    urls = (
        db.query(urls_model.URL)
            .filter(
                urls_model.URL.owner_id == current_user.id,
                urls_model.URL.is_deleted.is_(False))
            .all()
    )
    
    updated_url = []
    
    for url in urls:
        update_url = urls_schema.URLOutput.model_validate(url)
        update_url.shorten_url = f'{request.base_url}{update_url.shorten_url}'
        updated_url.append(update_url)
    
    return updated_url


# -------------------------------------------------
#                   DELETE - URL
# -------------------------------------------------

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_url(
        id: int,
        current_user: user_model.User = Depends(utils.get_current_user),
        db: Session = Depends(get_db)
    ):
    
    url = (
        db.query(urls_model.URL)
            .filter(
                urls_model.URL.id == id,
                urls_model.URL.is_deleted != True,
                urls_model.URL.owner_id == current_user.id)
            .first()
    )
    
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='url not found'
        )
    
    setattr(url, 'is_deleted', True)
    db.commit()