
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, pydantric_schemas, utils, oauth2

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model=pydantric_schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credantial")
    
   

    if not utils.verify(user_credential.password, user.passwd):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credantial")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token,"token_type" : "bearer" }
