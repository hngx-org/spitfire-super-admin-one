import json
import pytest
from flask import Flask
from super_admin_1.models.alternative import Database

# Create a Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

# Create a test client for the app
@pytest.fixture
def client(app):
    base_url = 'https://spitfire-superadmin-1.onrender.com'
    client = app.test_client()
    client.base_url = base_url
    return client

# Define a test for the GET /api/shop/endpoint route
def test_shop_endpoint(client):
    response = client.get('/api/shop/endpoint')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'This is the shop endpoint under /api/shop/endpoint'

# Define a test for the PUT /api/shop/ban_vendor/<uuid:user_id> route
def test_ban_vendor(client, monkeypatch):
    def mock_cursor():
        return

    monkeypatch.setattr(Database, '__enter__', mock_cursor)

    user_id = '6d49f12f-2295-423e-9de3-f945ee82d7f0'
    response = client.put(f'/api/shop/ban_vendor/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Vendor account banned temporarily.'

# Define a test for the GET /api/shop/banned_vendors route
def test_get_banned_vendors(client, monkeypatch):
    # Mock the Database class or relevant dependencies if needed
    def mock_cursor():
        return

    monkeypatch.setattr(Database, '__enter__', mock_cursor)

    response = client.get('/api/shop/banned_vendors')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'banned_vendors' in data


if __name__ == '__main__':
    pytest.main()
