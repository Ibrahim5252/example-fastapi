from app import pydantric_schemas
import pytest

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validation(posts):
        return pydantric_schemas.PostOut(**posts)
    post_map = map(validation, res.json())
    print(list(post_map))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_authorized_get_single_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = pydantric_schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200



def test_authorized_get_single_post_not_exists(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/1234567890")
    print(res.json())
    assert res.status_code == 404

def test_unauthorized_get_single_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 401

@pytest.mark.parametrize("title, content, published", [
    ("kane", "big red machine", True),
    ("john cena", "can't see him", True),
    ("undertaker", "deadman", True)
])
def test_create_post(authorized_client,test_user,test_posts, title, content, published):
    res = authorized_client.post("/posts/", json ={"title" : title, "content" : content, "published" : published})
    created_post = pydantric_schemas.Post(**res.json())
   
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user['id']

def test_create_default_published_true(authorized_client,test_user,test_posts):
    res = authorized_client.post("/posts/", json ={"title" : "shits", "content" : "wertyuihgfcvb"})
    created_post = pydantric_schemas.Post(**res.json())
   
    assert res.status_code == 201
    assert created_post.title == "shits"
    assert created_post.content == "wertyuihgfcvb"
    assert created_post.published == True
    
def test_unauthorized_create_post(client, test_posts):
    res = client.post("/posts/", json ={"title" : "shits", "content" : "wertyuihgfcvb"})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_delete_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 200

def test_authorized_delete_non_existed_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{12345678909876543}")
    print(res.json())
    assert res.status_code == 404

def test_authorized_delete_other_post(authorized_client,test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    print(res.json())
    assert res.status_code == 403

def test_authorized_update_post(authorized_client,test_posts, test_user):
    data = {
            "title" : "updated title.",
            "content" : "updated content"
            }
    
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = pydantric_schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_authorized_update_other_post(authorized_client,test_posts, test_user, test_user2):
    data = {
            "title" : "updated title.",
            "content" : "updated content"
            }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_posts,test_user2):
     data = {
             "title" : "updated title.",
             "content" : "updated content"
            }
     res = client.put(f"/posts/{test_posts[3].id}", json = data)
     assert res.status_code == 401


def test_authorized_update_non_existed_post(authorized_client,test_posts, test_user):
    data = {
            "title" : "updated title.",
            "content" : "updated content"
            }
    res = authorized_client.put(f"/posts/{1234567890}", json = data)
    assert res.status_code == 404
