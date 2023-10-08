import pytest
from super_admin_1 import create_app, db
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User

# Initialize the Flask app for testing
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

# Initialize the database for testing
@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

# Test case for deleting a shop
def test_delete_shop(app, database):
    # Create a test shop
    shop = Shop(name="Test Shop", merchant_id="550e8400-e29b-41d4-a716-446655440002", restricted="no", policy_confirmation=True,
            admin_status='pending', is_deleted='active', reviewed=False, rating=0)
    database.session.add(shop)
    database.session.commit()
    response = app.test_client().delete(f'/shop/{shop.id}')

    assert response.status_code == 200
    assert shop.is_deleted == 'temporary'

# Test case for creating a new user
def test_create_user(app, database):
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

    response = app.test_client().post('/user/create', json=user_data)

    assert response.status_code == 201

    user = User.query.filter_by(username=user_data["username"]).first()
    assert user is not None
