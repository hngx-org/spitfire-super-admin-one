import json
import pytest
from flask import Flask
from super_admin_1.products.delete_product import product_delete

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(product_delete)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_temporary_delete(client):
    # Create a test product ID
    test_product_id = "550e8400-e29b-41d4-a716-446655440003"

    # Test case 1: Successful temporary deletion
    response = client.patch(f'/api/product/{test_product_id}')
    assert response.status_code == 204
    data = json.loads(response.data)
    assert data['message'] == 'Product temporarily deleted'
    assert data['data'] is None

    # Test case 2: Product not found
    response = client.patch('/api/product/nonexistent_id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not Found'
    assert data['message'] == 'Product not found'

    # Test case 3: Internal Server Error during logging
    with pytest.raises(Exception):
        client.patch(f'/api/product/{test_product_id}')

def test_permanent_delete(client):
    # Create a test product ID
    test_product_id = "test_product_id"

    # Test case 1: Successful permanent deletion
    response = client.delete(f'/api/product/{test_product_id}')
    assert response.status_code == 204
    data = json.loads(response.data)
    assert data['message'] == 'Product permanently deleted'
    assert data['data'] is None

    # Test case 2: Product not found
    response = client.delete('/api/product/nonexistent_id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not Found'
    assert data['message'] == 'Product not found'

    # Test case 3: Internal Server Error during logging
    with pytest.raises(Exception):
        client.delete(f'/api/product/{test_product_id}')

def test_get_products(client):
    # Test case 1: Successful retrieval of products
    response = client.get('/api/product/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_log(client):
    # Test case 1: Successful log file download
    response = client.get('/api/product/download/log')
    assert response.status_code == 200

