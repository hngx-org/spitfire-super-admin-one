import pytest
from super_admin_1.models.shop_logs import ShopsLogs
from super_admin_1.shop.shoplog_helpers import ShopLogs

# Initialize the Flask app for testing (if needed)
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

# Test case for logging shop created
def test_log_shop_created():
    user_id = '550e8400-e29b-41d4-a716-446655440002'
    shop_id = '550e8400-e29b-41d4-a716-446655440001'

    shop_logs = ShopLogs(user_id, shop_id)

    shop_logs.log_shop_created()

    created_log = ShopsLogs.query.filter_by(shop_id=shop_id, action='created').first()
    assert created_log is not None


if __name__ == '__main__':
    pytest.main()
