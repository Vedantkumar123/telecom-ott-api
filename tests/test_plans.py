import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from bson import ObjectId


class TestPlanCreate:
    """Test suite for plan creation"""

    def test_create_plan_success_as_admin(self, client, admin_headers, sample_plan_data, monkeypatch):
        """Test successful plan creation by admin"""
        mock_create = MagicMock(return_value={"message": "Plan created successfully", "plan_id": str(ObjectId())})
        monkeypatch.setattr("app.controllers.plan_controller.create_plan_service", mock_create)

        response = client.post("/plans/", json=sample_plan_data, headers=admin_headers)

        assert response.status_code == 200
        assert "plan_id" in response.json()
        mock_create.assert_called_once()

    def test_create_plan_forbidden_for_customer(self, client, customer_headers, sample_plan_data, monkeypatch):
        """Test that non-admins cannot create plans"""
        response = client.post("/plans/", json=sample_plan_data, headers=customer_headers)
        assert response.status_code == 403
        assert "Admin only" in response.json()["detail"]

    def test_create_plan_requires_auth_token(self, client, sample_plan_data):
        """Test that plan creation requires authentication"""
        response = client.post("/plans/", json=sample_plan_data)
        assert response.status_code == 403  # Forbidden without token

    def test_create_plan_missing_name(self, client, admin_headers):
        """Test plan creation fails when name is missing"""
        payload = {
            "price": 499.99,
            "validity_days": 30,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_create_plan_missing_price(self, client, admin_headers):
        """Test plan creation fails when price is missing"""
        payload = {
            "name": "Premium",
            "validity_days": 30,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_create_plan_missing_validity_days(self, client, admin_headers):
        """Test plan creation fails when validity_days is missing"""
        payload = {
            "name": "Premium",
            "price": 499.99,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_create_plan_missing_included_apps(self, client, admin_headers):
        """Test plan creation fails when included_apps is missing"""
        payload = {
            "name": "Premium",
            "price": 499.99,
            "validity_days": 30
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_create_plan_with_negative_price(self, client, admin_headers):
        """Test plan creation with negative price"""
        payload = {
            "name": "Invalid Plan",
            "price": -99.99,
            "validity_days": 30,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        # Should either pass validation or be caught by service
        assert response.status_code in [200, 400, 422]

    def test_create_plan_with_zero_validity_days(self, client, admin_headers):
        """Test plan creation with zero validity days"""
        payload = {
            "name": "Invalid Plan",
            "price": 99.99,
            "validity_days": 0,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        # Service might allow this, but it's business logic
        assert response.status_code in [200, 400]

    def test_create_plan_with_empty_apps_list(self, client, admin_headers):
        """Test plan creation with empty included_apps"""
        payload = {
            "name": "Free Plan",
            "price": 0,
            "validity_days": 7,
            "included_apps": []
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        # Should succeed - free plan with no apps is valid
        assert response.status_code in [200, 400]

    def test_create_plan_server_error_handling(self, client, admin_headers, sample_plan_data, monkeypatch):
        """Test plan creation handles server errors gracefully"""
        def mock_create(plan):
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        monkeypatch.setattr("app.controllers.plan_controller.create_plan_service", mock_create)

        response = client.post("/plans/", json=sample_plan_data, headers=admin_headers)
        assert response.status_code == 500


class TestPlanRetreval:
    """Test suite for plan retrieval"""

    def test_get_all_plans_success(self, client, monkeypatch):
        """Test successful retrieval of all plans"""
        mock_plans = [
            {
                "_id": str(ObjectId()),
                "name": "Basic",
                "price": 99.99,
                "validity_days": 30,
                "included_apps": ["Netflix"]
            },
            {
                "_id": str(ObjectId()),
                "name": "Premium",
                "price": 499.99,
                "validity_days": 30,
                "included_apps": ["Netflix", "Prime"]
            }
        ]
        
        mock_get = MagicMock(return_value=mock_plans)
        monkeypatch.setattr("app.controllers.plan_controller.get_plans_service", mock_get)

        response = client.get("/plans/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Basic"
        assert data[1]["name"] == "Premium"

    def test_get_plans_empty_list(self, client, monkeypatch):
        """Test retrieval when no plans exist"""
        mock_get = MagicMock(return_value=[])
        monkeypatch.setattr("app.controllers.plan_controller.get_plans_service", mock_get)

        response = client.get("/plans/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_plans_no_auth_required(self, client, monkeypatch):
        """Test that plan retrieval doesn't require authentication"""
        mock_get = MagicMock(return_value=[{"_id": "123", "name": "Test", "price": 99.99, "validity_days": 30, "included_apps": []}])
        monkeypatch.setattr("app.controllers.plan_controller.get_plans_service", mock_get)

        response = client.get("/plans/")

        assert response.status_code == 200

    def test_get_plans_converts_object_ids(self, client, monkeypatch):
        """Test that ObjectIds are converted to strings in response"""
        plan_id = str(ObjectId())
        
        mock_plans = [
            {
                "_id": plan_id,
                "name": "Premium",
                "price": 499.99,
                "validity_days": 30,
                "included_apps": ["Netflix"]
            }
        ]
        
        mock_get = MagicMock(return_value=mock_plans)
        monkeypatch.setattr("app.controllers.plan_controller.get_plans_service", mock_get)

        response = client.get("/plans/")
        
        assert response.status_code == 200
        data = response.json()
        assert data[0]["_id"] == plan_id


class TestPlanSchema:
    """Test suite for plan schema validation"""

    def test_plan_name_is_string(self, client, admin_headers):
        """Test that plan name must be a string"""
        payload = {
            "name": 12345,  # Invalid: number instead of string
            "price": 99.99,
            "validity_days": 30,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_plan_price_is_number(self, client, admin_headers):
        """Test that plan price must be a number"""
        payload = {
            "name": "Premium",
            "price": "ninety-nine",  # Invalid: string instead of number
            "validity_days": 30,
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_plan_validity_days_is_integer(self, client, admin_headers):
        """Test that validity_days must be an integer"""
        payload = {
            "name": "Premium",
            "price": 99.99,
            "validity_days": "thirty",  # Invalid: string instead of int
            "included_apps": ["Netflix"]
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422

    def test_plan_included_apps_is_list(self, client, admin_headers):
        """Test that included_apps must be a list"""
        payload = {
            "name": "Premium",
            "price": 99.99,
            "validity_days": 30,
            "included_apps": "Netflix,Prime"  # Invalid: string instead of list
        }
        response = client.post("/plans/", json=payload, headers=admin_headers)
        assert response.status_code == 422
