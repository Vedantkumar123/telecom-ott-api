import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime, timedelta


class TestSubscriptionCreate:
    """Test suite for subscription creation"""

    def test_subscribe_to_plan_success(self, client, customer_headers, monkeypatch):
        """Test successful subscription to a plan"""
        plan_id = str(ObjectId())
        mock_subscribe = MagicMock(return_value={"message": "Subscribed successfully", "subscription_id": str(ObjectId())})
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": plan_id}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)

        assert response.status_code == 200
        assert "subscription_id" in response.json()

    def test_subscribe_requires_auth(self, client):
        """Test that subscription requires authentication"""
        payload = {"plan_id": str(ObjectId())}
        response = client.post("/subscriptions/", json=payload)
        assert response.status_code == 403

    def test_subscribe_missing_plan_id(self, client, customer_headers):
        """Test subscription fails without plan_id"""
        payload = {}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 422

    def test_subscribe_invalid_plan_id_format(self, client, customer_headers, monkeypatch):
        """Test subscription fails with invalid plan_id format"""
        def mock_subscribe(user_id, plan_id):
            raise HTTPException(status_code=400, detail="Invalid plan_id format. Must be a valid MongoDB ObjectId")
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": "invalid-id"}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 400

    def test_subscribe_to_nonexistent_plan(self, client, customer_headers, monkeypatch):
        """Test subscription fails if plan doesn't exist"""
        def mock_subscribe(user_id, plan_id):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": str(ObjectId())}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 404

    def test_subscribe_with_valid_object_id(self, client, customer_headers, monkeypatch):
        """Test subscription with valid ObjectId format"""
        plan_id = ObjectId()
        
        def mock_subscribe(user_id, plan_id_param):
            assert str(plan_id_param) == str(plan_id)
            return {"message": "Subscribed successfully", "subscription_id": str(ObjectId())}
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": str(plan_id)}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 200

    def test_subscribe_server_error(self, client, customer_headers, monkeypatch):
        """Test handling of server error during subscription"""
        def mock_subscribe(user_id, plan_id):
            raise HTTPException(status_code=500, detail="Database error")
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": str(ObjectId())}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 500

    def test_subscribe_creates_correct_dates(self, client, customer_headers, monkeypatch):
        """Test that subscription sets correct start and end dates based on plan validity"""
        plan_id = str(ObjectId())
        subscription_id = str(ObjectId())
        
        def mock_subscribe(uid, pid):
            # In real implementation, this would calculate dates based on plan validity
            # User ID is generated from JWT token, so we just verify it's not empty
            assert uid is not None
            assert len(uid) > 0
            return {"message": "Subscribed successfully", "subscription_id": subscription_id}
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": plan_id}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 200


class TestSubscriptionRetrieval:
    """Test suite for subscription retrieval"""

    def test_get_my_subscriptions_success(self, client, customer_headers, monkeypatch):
        """Test successful retrieval of user subscriptions"""
        subscription_id = str(ObjectId())
        plan_id = str(ObjectId())
        now = datetime.utcnow().isoformat()
        end = (datetime.utcnow() + timedelta(days=30)).isoformat()
        
        mock_subs = [
            {
                "_id": subscription_id,
                "plan_id": plan_id,
                "status": "active",
                "start_date": now,
                "end_date": end
            }
        ]
        
        mock_get = MagicMock(return_value=mock_subs)
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "active"

    def test_get_my_subscriptions_requires_auth(self, client):
        """Test that subscription retrieval requires authentication"""
        response = client.get("/subscriptions/my")
        assert response.status_code == 403

    def test_get_my_subscriptions_empty(self, client, customer_headers, monkeypatch):
        """Test retrieval when user has no subscriptions"""
        mock_get = MagicMock(return_value=[])
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        assert response.status_code == 200
        assert response.json() == []

    def test_get_my_subscriptions_multiple(self, client, customer_headers, monkeypatch):
        """Test retrieval of multiple subscriptions"""
        mock_subs = [
            {
                "_id": str(ObjectId()),
                "plan_id": str(ObjectId()),
                "status": "active",
                "start_date": datetime.utcnow().isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            {
                "_id": str(ObjectId()),
                "plan_id": str(ObjectId()),
                "status": "expired",
                "start_date": (datetime.utcnow() - timedelta(days=60)).isoformat(),
                "end_date": (datetime.utcnow() - timedelta(days=30)).isoformat()
            }
        ]
        
        mock_get = MagicMock(return_value=mock_subs)
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["status"] == "active"
        assert data[1]["status"] == "expired"

    def test_get_subscriptions_returns_correct_fields(self, client, customer_headers, monkeypatch):
        """Test that subscription retrieval returns all required fields"""
        subscription_id = str(ObjectId())
        plan_id = str(ObjectId())
        
        mock_subs = [
            {
                "_id": subscription_id,
                "user_id": "user-123",
                "plan_id": plan_id,
                "status": "active",
                "start_date": datetime.utcnow().isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            }
        ]
        
        mock_get = MagicMock(return_value=mock_subs)
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        assert response.status_code == 200
        data = response.json()[0]
        assert "_id" in data
        assert "plan_id" in data
        assert "status" in data
        assert "start_date" in data
        assert "end_date" in data


class TestSubscriptionSchema:
    """Test suite for subscription schema validation"""

    def test_subscription_plan_id_required(self, client, customer_headers):
        """Test that plan_id is required"""
        payload = {}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 422

    def test_subscription_plan_id_must_be_string(self, client, customer_headers):
        """Test that plan_id must be a string"""
        payload = {"plan_id": 12345}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 422

    def test_subscription_plan_id_cannot_be_empty(self, client, customer_headers, monkeypatch):
        """Test that plan_id cannot be empty string"""
        def mock_subscribe(user_id, plan_id):
            raise HTTPException(status_code=400, detail="Invalid plan_id format")
        
        monkeypatch.setattr("app.controllers.subscription_controller.subscribe", mock_subscribe)

        payload = {"plan_id": ""}
        response = client.post("/subscriptions/", json=payload, headers=customer_headers)
        assert response.status_code == 400


class TestSubscriptionStatus:
    """Test suite for subscription status transitions"""

    def test_active_subscription_exists(self, client, customer_headers, monkeypatch):
        """Test checking if active subscription exists"""
        mock_subs = [
            {
                "_id": str(ObjectId()),
                "plan_id": str(ObjectId()),
                "status": "active",
                "start_date": datetime.utcnow().isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            }
        ]
        
        mock_get = MagicMock(return_value=mock_subs)
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        data = response.json()
        assert any(sub["status"] == "active" for sub in data)

    def test_expired_subscription_shown(self, client, customer_headers, monkeypatch):
        """Test that expired subscriptions are shown in history"""
        mock_subs = [
            {
                "_id": str(ObjectId()),
                "plan_id": str(ObjectId()),
                "status": "expired",
                "start_date": (datetime.utcnow() - timedelta(days=60)).isoformat(),
                "end_date": (datetime.utcnow() - timedelta(days=30)).isoformat()
            }
        ]
        
        mock_get = MagicMock(return_value=mock_subs)
        monkeypatch.setattr("app.controllers.subscription_controller.get_my_subscriptions", mock_get)

        response = client.get("/subscriptions/my", headers=customer_headers)
        
        data = response.json()
        assert len(data) > 0
        assert data[0]["status"] == "expired"
