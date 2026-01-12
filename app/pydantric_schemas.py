from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy import Integer, Null
from typing import Optional, Literal


class PostBase(BaseModel):
    id : Optional[int]= None
    title : str
    content : str
    published : bool=True


class CreatePost(BaseModel):
    title : str
    content : str
    
class ShowUser(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

class Post(PostBase):
    # owner_id : int
    owner : ShowUser

    class Config:       #!<-this take the SQLalchemy output and read it even though it is not dict (pydantic only take dicts).
        orm_mode = True #!<- 

class PostOut(BaseModel):
    Post: Post
    votes : int

    class Config:       #!<-this take the SQLalchemy output and read it even though it is not dict (pydantic only take dicts).
        orm_mode = True #!<-

class UserCreate(BaseModel):
    email : EmailStr
    passwd : str

    class Config:       #!<-this take the SQLalchemy output and read it even though it is not dict (pydantic only take dicts).
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    passwd : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir : Literal[0,1]