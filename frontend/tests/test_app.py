import pytest
from app import app, posts_collection
from bson import ObjectId

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_post(client):
    response = client.post('/create', data=dict(
        title='New Test Post',
        content='This is a new test post.',
        scale='test_scale'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_edit_post(client):
    post_id = posts_collection.insert_one({
        'title': 'Test Post',
        'content': 'This is a test post.',
        'scale': 'test_scale'
    }).inserted_id

    response = client.post(f'/edit_post/{post_id}', data=dict(
        title='Updated Test Post',
        content='This is an updated test post.'
    ), follow_redirects=True)
    assert response.status_code == 200

def test_delete_post(client):
    post_id = posts_collection.insert_one({
        'title': 'Test Post',
        'content': 'This is a test post.',
        'scale': 'test_scale'
    }).inserted_id

    response = client.post(f'/delete_post/{post_id}', follow_redirects=True)
    assert response.status_code == 200
