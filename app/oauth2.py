from tokenize import Token
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import pydantric_schemas, database, models, config



SECRET_KEY = config.settings.secret_key or ""
ALGORITHM = config.settings.algorithm or ""
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes or 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    
    return encoded_jwt



def verify_access_token(token: str, credential_expectation):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_expectation
        token_data: pydantric_schemas.TokenData = pydantric_schemas.TokenData(id=str(id))
    
    except JWTError:
        raise credential_expectation
    
    return token_data

def get_currrnt_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

  credential_expectation = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credential",
                                         headers={"WWW-Authenticate": "Bearer"})

  token_data = verify_access_token(token, credential_expectation)
  user = db.query(models.User).filter(models.User.id == int(token_data.id)).first() if token_data.id else None

  return user
  