from fastapi import FastAPI
from app.router import auth
from . import models
from .database import engine
from .router import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
#! ROOT.#########################################################################################
@app.get("/")
def root():
    return {"message": "Heloo world!!"}


app.include_router(user.router) #!<- this is use to include the post file which is in router so it responds the app and calls.
app.include_router(post.router) #!   so in post & user file will have "@router.get" rather than "@app.get".
app.include_router(auth.router)
app.include_router(vote.router)



