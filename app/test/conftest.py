import pytest
from app.database import get_db
from app.models import Base
from fastapi.testclient import TestClient
from app.main import app
from .databse import TestingSessionLocal, engine
from app.oauth2 import create_access_token
from app import models

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 



@pytest.fixture
def client(session):
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close() 
    app.dependency_overrides[get_db] = override_get_db   
    # it will run this command ^ before running test.
    yield TestClient(app) #! this is done with the help of "yield" keyword
    # it will run the below command after running the test.
    
@pytest.fixture
def test_user(client):
    user_data = {"email" : "helo@gmail.com", "passwd" : "1234567890"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password']=user_data['passwd']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email" : "john@gmail.com", "passwd" : "12345678901234567890"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password']=user_data['passwd']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title" : "1st title.",
            "content" : "1st content",
            "owner_id" : test_user['id']
        },

        {
            "title" : "2nd title.",
            "content" : "2nd content",
            "owner_id" : test_user['id']
        },

        {
            "title" : "3rd title.",
            "content" : "3rd content",
            "owner_id" : test_user['id']
        },

        {
            "title" : "4rd title.",
            "content" : "4rd content",
            "owner_id" : test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts_list = list(post_map)

    session.add_all(posts_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

