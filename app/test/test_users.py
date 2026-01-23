from app import pydantric_schemas
from jose import jwt
from app.config import settings
import pytest



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'heloo world!!'
#     assert res.status_code == 200



def test_create_user(client):
    res = client.post("/users/", json={"email" : "helo@gmail.com", "passwd" : "1234567890"})
    print(res)
    assert res.status_code == 201
    

def test_login_user(test_user, client):
    res = client.post("/login", data={"username" : test_user['email'], "password" : test_user['password']})
    login_res = pydantric_schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# "email" : "helo@gmail.com", "passwd" : "1234567890"}
@pytest.mark.parametrize("email, password, status_code", [
    ("helo@gmail.com", "wrongpasswd", 403),
    ("wrong@gmail.com","1234567890", 403),
    ("wrong@gmail.com", "wrongpasswd", 403),
    (None, "1234567890", 422),
     ("helo@gmail.com", None, 422)
])
def test_incorrect_login(client,email, password, status_code):
    res = client.post("/login", data={"username" : email, "password" : password})
    assert res.status_code == status_code



