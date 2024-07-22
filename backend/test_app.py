import json
from bson import ObjectId

from app import app, posts_collection


def test_health_check():
  """Tests the health check route."""
  with app.test_client() as client:
    response = client.get('/check')
    assert response.status_code == 200
    assert response.json == {'message': "Hello, World! This is the backend."}


def test_get_all_posts_empty():
  """Tests retrieving all posts (empty collection)."""
  # No setup needed, empty collection by default

  with app.test_client() as client:
    response = client.get('/posts')
    assert response.status_code == 200
    assert response.json == []


def test_get_all_posts_populated(sample_posts):
  """Tests retrieving all posts (populated collection)."""
  # Use fixture (sample_posts) to populate collection before test

  with app.test_client() as client:
    response = client.get('/posts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == len(sample_posts)  # Assert number of posts match


def test_get_post_by_id_success(sample_post):
  """Tests retrieving a post by its ID (success case)."""
  post_id = str(sample_post['_id'])  # Convert ObjectId to string

  with app.test_client() as client:
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['_id'] == post_id
    assert data['title'] == sample_post['title']
    assert data['content'] == sample_post['content']


def test_get_post_by_id_fail():
  """Tests retrieving a post by a non-existent ID (failure case)."""
  invalid_id = 'invalid_id'

  with app.test_client() as client:
    response = client.get(f'/posts/{invalid_id}')
    assert response.status_code == 404
    assert response.json == {'error': 'Post not found'}


def test_create_post(new_post_data):
  """Tests creating a new post."""
  with app.test_client() as client:
    response = client.post('/posts', json=new_post_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == new_post_data['title']
    assert data['content'] == new_post_data['content']
    assert data.get('scale') == new_post_data.get('scale', 'default_scale_value')  # Check for default value

  # Cleanup the test data (assuming you don't need the data)
  posts_collection.delete_one({'_id': ObjectId(data['_id'])})


def test_update_post_success(sample_post, updated_post_data):
  """Tests updating a post (success case)."""
  post_id = str(sample_post['_id'])

  with app.test_client() as client:
    response = client.put(f'/posts/{post_id}', json=updated_post_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['_id'] == post_id
    assert data['title'] == updated_post_data['title']
    assert data['content'] == updated_post_data['content']


def test_update_post_fail(sample_post, non_existent_id):
  """Tests updating a post with a non-existent ID (failure case)."""
  with app.test_client() as client:
    response = client.put(f'/posts/{non_existent_id}', json=sample_post)
    assert response.status_code == 404
    assert response.json == {'error': 'Post not found'}


def test_delete_post_success(sample_post):
  """Tests deleting a post (success case)."""
  post_id = str
