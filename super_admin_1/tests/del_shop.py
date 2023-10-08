import json
import pytest
from flask import Flask
from super_admin_1 import db, create_app
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User
from super_admin_1.models.shop_logs import ShopsLogs

# Create a Flask app for testing
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

# Create a test client for the app
@pytest.fixture
def client(app):
    base_url = 'https://spitfire-superadmin-1.onrender.com'
    client = app.test_client()
    client.base_url = base_url
    return client

# Define a test for the DELETE /shop/<shop_id> route
def test_delete_shop(client, monkeypatch):
    def mock_cursor():
        return

    monkeypatch.setattr(db, '__enter__', mock_cursor)

    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.delete(f'/shop/{shop_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Shop temporarily deleted.'

# Define a test for the POST /user/create route
def test_create_user(client):
    user_data = {
        "username": "testuser",
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "section_order": 1,
        "password": "testpassword",
        "is_verified": True,
        "two_factor_auth": False,
        "provider": "local",
        "profile_pic": "test.jpg",
        "refresh_token": "refreshtoken"
    }

    response = client.post('/user/create', json=user_data)

    assert response.status_code == 201
    user = User.query.filter_by(username=user_data["username"]).first()
    assert user is not None

# Define a test for the POST /user/<user_id>/shop route
def test_create_shop(client):
    user_id = '550e8400-e29b-41d4-a716-446655440002'
    shop_data = {
        "name": "Test Shop",
        "policy_confirmation": True,
        "reviewed": False,
        "rating": 0
    }

    response = client.post(f'/user/{user_id}/shop', json=shop_data)

    assert response.status_code == 201
    shop = Shop.query.filter_by(name=shop_data["name"]).first()
    assert shop is not None

# Define a test for the GET /shop and GET /shop/<shop_id> routes
def test_get_shop(client):
    # Test GET /shop
    response = client.get('/shop')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'shops' in data

    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.get(f'/shop/{shop_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'shop' in data

# Define a test for the DELETE /user/<user_id> route
def test_delete_user(client):
    user_id = '550e8400-e29b-41d4-a716-446655440002'

    response = client.delete(f'/user/{user_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'User deleted.'

# Define a test for the GET /logs/shops and GET /logs/shops/<shop_id> routes
def test_get_shop_logs(client):
    response = client.get('/logs/shops')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'logs' in data

    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.get(f'/logs/shops/{shop_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'logs' in data

# Define a test for the GET /logs/shops/download and GET /logs/shops/<shop_id>/download routes
def test_download_shop_logs(client):
    response = client.get('/logs/shops/download')
    assert response.status_code == 200

    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.get(f'/logs/shops/{shop_id}/download')
    assert response.status_code == 200

# Define a test for the PATCH /shop/<shop_id> route
def test_restore_shop(client, monkeypatch):
    def mock_cursor():
        return
    monkeypatch.setattr(db, '__enter__', mock_cursor)
    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.patch(f'/shop/{shop_id}', json={"is_deleted": "temporary"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Shop restored successfully.'

    # Test when the shop is not marked as deleted
    shop_id = '550e8400-e29b-41d4-a716-446655440001'
    response = client.patch(f'/shop/{shop_id}', json={"is_deleted": "active"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Shop is not marked as deleted.'

if __name__ == '__main__':
    pytest.main()
