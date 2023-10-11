import pytest
from super_admin_1 import create_app
import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_protected_resource_without_authentication(client):
    response = client.get("/api/shop/endpoint")
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data["error"] == "Unauthorized"
    assert data["message"] == "You are not logged in"
