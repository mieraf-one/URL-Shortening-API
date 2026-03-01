import string
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import urls as urls_model
from random import choices

def url_gen(original_url: str, custom_url: str, db: Session, owner_id: int):   
    if custom_url:
        # fetch url
        url = db.query(urls_model.URL).filter(urls_model.URL.shorten_url == custom_url).first()
        
        # check if url already exists
        if url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='url already existed'
            )
        
        # insert custom url into db
        new_url = urls_model.URL(owner_id=owner_id, original_url=original_url, shorten_url=custom_url)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        
        return new_url
    
    
    count = 0
    while True:
        generated_url = ''.join(choices([*string.ascii_letters, *string.digits], k=5))
        
        # fetch url
        url = db.query(urls_model.URL).filter(urls_model.URL.shorten_url == generated_url).first()
        
        # check if url already exists
        if url is None:
            break
        
        # raise an error if took too much checking
        if count > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='please try again'
            )
        
        count += 1
    
    # insert custom url into db
    new_url = urls_model.URL(owner_id=owner_id, original_url=original_url, shorten_url=generated_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    
    return new_url
