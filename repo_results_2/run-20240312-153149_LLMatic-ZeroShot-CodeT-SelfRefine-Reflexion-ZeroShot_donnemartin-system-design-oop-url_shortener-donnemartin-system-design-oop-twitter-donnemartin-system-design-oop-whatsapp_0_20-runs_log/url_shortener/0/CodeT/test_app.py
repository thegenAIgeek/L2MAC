import pytest
import app
from flask import json

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	with app.app.test_client() as client:
		yield client


def test_create_user(client):
	response = client.post('/create_user')
	assert response.status_code == 201
	data = json.loads(response.data)
	assert 'user_id' in data


def test_create_url(client):
	response = client.post('/create_user')
	user_id = json.loads(response.data)['user_id']
	response = client.post('/create_url', json={'user_id': user_id, 'original_url': 'https://www.google.com'})
	assert response.status_code == 201
	data = json.loads(response.data)
	assert 'url_id' in data
	assert 'short_url' in data


def test_redirect_url(client):
	response = client.post('/create_user')
	user_id = json.loads(response.data)['user_id']
	response = client.post('/create_url', json={'user_id': user_id, 'original_url': 'https://www.google.com'})
	short_url = json.loads(response.data)['short_url']
	response = client.get(f'/{short_url}')
	assert response.status_code == 302


def test_get_analytics(client):
	response = client.post('/create_user')
	user_id = json.loads(response.data)['user_id']
	response = client.post('/create_url', json={'user_id': user_id, 'original_url': 'https://www.google.com'})
	response = client.get(f'/analytics/{user_id}')
	assert response.status_code == 200
	data = json.loads(response.data)
	assert len(data) == 1