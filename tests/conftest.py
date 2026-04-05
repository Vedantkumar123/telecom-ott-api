import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from bson import ObjectId
from datetime import datetime, timedelta

from app.main import app
from app.core.security import create_token, hash_password


@pytest.fixture
def client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture
def admin_token():
    """Fixture for admin user token"""
    return create_token({"user_id": str(ObjectId()), "role": "admin"})


@pytest.fixture
def customer_token():
    """Fixture for customer user token"""
    return create_token({"user_id": str(ObjectId()), "role": "customer"})


@pytest.fixture
def admin_headers(admin_token):
    """Fixture for admin authentication headers"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def customer_headers(customer_token):
    """Fixture for customer authentication headers"""
    return {"Authorization": f"Bearer {customer_token}"}


@pytest.fixture
def sample_user_data():
    """Fixture for sample user registration data"""
    return {
        "mobile_number": "9876543210",
        "password": "TestPassword123",
        "role": "customer"
    }


@pytest.fixture
def sample_admin_data():
    """Fixture for sample admin registration data"""
    return {
        "mobile_number": "9999999999",
        "password": "AdminPassword123",
        "role": "admin"
    }


@pytest.fixture
def sample_plan_data():
    """Fixture for sample plan data"""
    return {
        "name": "Premium Plan",
        "price": 499.99,
        "validity_days": 30,
        "included_apps": ["Netflix", "Prime Video", "Disney+"]
    }


@pytest.fixture
def sample_content_data():
    """Fixture for sample content data"""
    return {
        "title": "The Midnight Club",
        "platform": "Netflix",
        "category": "Movies"
    }


@pytest.fixture
def mock_db_user():
    """Fixture for mocked user document from database"""
    user_id = str(ObjectId())
    return {
        "_id": ObjectId(),
        "mobile_number": "9876543210",
        "password": hash_password("TestPassword123"),
        "role": "customer",
        "is_active": True
    }


@pytest.fixture
def mock_db_plan():
    """Fixture for mocked plan document from database"""
    return {
        "_id": ObjectId(),
        "name": "Premium Plan",
        "price": 499.99,
        "validity_days": 30,
        "included_apps": ["Netflix", "Prime Video", "Disney+"]
    }


@pytest.fixture
def mock_db_content():
    """Fixture for mocked content document from database"""
    return {
        "_id": ObjectId(),
        "title": "The Midnight Club",
        "platform": "Netflix",
        "category": "Movies"
    }


@pytest.fixture
def mock_db_subscription():
    """Fixture for mocked subscription document from database"""
    now = datetime.utcnow()
    return {
        "_id": ObjectId(),
        "user_id": str(ObjectId()),
        "plan_id": str(ObjectId()),
        "start_date": now,
        "end_date": now + timedelta(days=30),
        "status": "active"
    }


@pytest.fixture
def mock_db_access_log():
    """Fixture for mocked access log document from database"""
    return {
        "_id": ObjectId(),
        "user_id": str(ObjectId()),
        "content_id": str(ObjectId()),
        "watched_at": datetime.utcnow()
    }


@pytest.fixture(autouse=True)
def mock_jwt_secret(monkeypatch):
    """Fixture to ensure JWT secret is set for all tests"""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-for-testing-only")
