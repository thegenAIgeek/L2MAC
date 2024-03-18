import pytest
import app

@pytest.fixture
def client():
	app.app.config['TESTING'] = True
	with app.app.test_client() as client:
		yield client


def test_create_short_url(client):
	response = client.post('/', json={'long_url': 'https://www.google.com'})
	assert response.status_code == 201
	assert 'short_url' in response.get_json()


def test_redirect_to_long_url(client):
	response = client.post('/', json={'long_url': 'https://www.google.com'})
	short_url = response.get_json()['short_url']
	response = client.get(f'/{short_url}')
	assert response.status_code == 302
	assert response.location == 'https://www.google.com'


def test_redirect_to_non_existent_url(client):
	response = client.get('/non_existent')
	assert response.status_code == 404