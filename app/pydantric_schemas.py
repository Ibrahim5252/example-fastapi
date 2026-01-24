from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal

# We use ConfigDict at the top level or inside specific models 
# to allow Pydantic to read SQLAlchemy models (ORM)

class PostBase(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True

class CreatePost(BaseModel):
    title: str
    content: str

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # New V2 way to enable ORM mode
    model_config = ConfigDict(from_attributes=True)

class Post(PostBase):
    owner: ShowUser
    
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    passwd: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    passwd: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]