import json
import pytest
from flask import Flask
from super_admin_1 import db, create_app
from super_admin_1.models.shop import Shop

# Create a Flask app for testing
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

# Create a test client for the app
@pytest.fixture
def client(app):
    client = app.test_client()
    return client

# Initialize and clean up the database for each test
@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

# Define a test for the unban_vendor endpoint
def test_unban_vendor(client, init_database):
    vendor = Shop(
    merchant_id="550e8400-e29b-41d4-a716-446655440001",
    name="Test Vendor",
    policy_confirmation=True,
    restricted="temporary",  # Simulate a banned vendor
    admin_status="pending",  # Simulate a pending status
    is_deleted="active",
    reviewed=False,
    rating=0.0,
)
    init_database.session.add(vendor)
    init_database.session.commit()

    # Define the vendor_id to unban
    vendor_id = vendor.id

    # Send a PUT request to unban the vendor
    response = client.put(f'/unban_vendor/{vendor_id}')

    # Check if the response status code is 200 (Success)
    assert response.status_code == 200

    # Check if the response message indicates success
    data = json.loads(response.data)
    assert data['status'] == 'Success'
    assert data['message'] == 'Vendor unbanned successfully.'

    # Check if the vendor's restricted and admin_status fields have been updated
    updated_vendor = Shop.query.get(vendor_id)
    assert updated_vendor.restricted == 'no'  # Should be unbanned
    assert updated_vendor.admin_status == 'approved'  # Should be updated


if __name__ == '__main__':
    pytest.main()
