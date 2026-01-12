from fastapi import status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, pydantric_schemas, utils



#! =========================================================================================
#? ============================= USER AUTHENTICATION SECTION ===============================
#! =========================================================================================
#? This section handles user authentication

router = APIRouter(
    prefix = "/users" , #!<-we use this so we can avoid writing same thing "/users" in every decorater and write once and just leave "/" or "/{id}".
    tags = ['Users']   #!<-this done for fastAPI docs so we can have all Users in seperate section rather than having it in default section.
)

#! CREATE USER.#########################################################################################
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=pydantric_schemas.ShowUser)
def create_user(user : pydantric_schemas.UserCreate, db : Session = Depends(get_db)):

    # hash the passwd - user passwd
    hashed_passwd = utils.hash(user.passwd)
    user.passwd = hashed_passwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


#! GET 1 USER VIA ID.#########################################################################################
@router.get('/{id}', response_model=pydantric_schemas.ShowUser)
def get_user_via_id(id : int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} does not exist.")
    return user