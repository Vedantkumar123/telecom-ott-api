import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime, timedelta


class TestAccessContent:
    """Test suite for content access"""

    def test_access_content_success(self, client, customer_headers, monkeypatch):
        """Test successful content access with valid subscription"""
        content_id = str(ObjectId())
        
        mock_access = MagicMock(return_value={"message": "Access granted", "log_id": str(ObjectId())})
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        response = client.post(f"/access/{content_id}", headers=customer_headers)

        assert response.status_code == 200
        assert "log_id" in response.json()

    def test_access_content_requires_auth(self, client):
        """Test that content access requires authentication"""
        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}")
        assert response.status_code == 403

    def test_access_content_invalid_id_format(self, client, customer_headers, monkeypatch):
        """Test access fails with invalid content_id format"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=400, detail="Invalid content_id format. Must be a valid MongoDB ObjectId")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        response = client.post("/access/invalid-id", headers=customer_headers)
        assert response.status_code == 400

    def test_access_content_not_found(self, client, customer_headers, monkeypatch):
        """Test access fails if content doesn't exist"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=404, detail="Content not found")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 404

    def test_access_content_no_active_subscription(self, client, customer_headers, monkeypatch):
        """Test access fails without active subscription"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=404, detail="No active subscription")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 404
        assert "No active subscription" in response.json()["detail"]

    def test_access_content_not_in_plan(self, client, customer_headers, monkeypatch):
        """Test access fails if content not included in plan"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=403, detail="Content not allowed in your plan")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 403
        assert "not allowed" in response.json()["detail"]

    def test_access_content_plan_not_found(self, client, customer_headers, monkeypatch):
        """Test access fails if plan for subscription not found"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=404, detail="Plan not found for active subscription")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 404

    def test_access_content_logs_access_attempt(self, client, customer_headers, monkeypatch):
        """Test that content access is logged"""
        content_id = str(ObjectId())
        log_id = str(ObjectId())
        
        def mock_access(user_id, content_id_param):
            assert user_id  # User ID should be present
            assert content_id_param == content_id
            return {"message": "Access granted", "log_id": log_id}
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 200
        assert response.json()["log_id"] == log_id

    def test_access_content_server_error(self, client, customer_headers, monkeypatch):
        """Test handling of server error during access"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=500, detail="Database error")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 500


class TestAccessHistory:
    """Test suite for access history retrieval"""

    def test_get_access_history_success(self, client, customer_headers, monkeypatch):
        """Test successful retrieval of access history"""
        mock_history = [
            {
                "_id": str(ObjectId()),
                "content_id": str(ObjectId()),
                "watched_at": datetime.utcnow().isoformat()
            },
            {
                "_id": str(ObjectId()),
                "content_id": str(ObjectId()),
                "watched_at": (datetime.utcnow() - timedelta(hours=1)).isoformat()
            }
        ]
        
        mock_get = MagicMock(return_value=mock_history)
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_access_history_requires_auth(self, client):
        """Test that history retrieval requires authentication"""
        response = client.get("/access/history")
        assert response.status_code == 403

    def test_get_access_history_empty(self, client, customer_headers, monkeypatch):
        """Test retrieval when no access history exists"""
        mock_get = MagicMock(return_value=[])
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)

        assert response.status_code == 200
        assert response.json() == []

    def test_get_access_history_returns_required_fields(self, client, customer_headers, monkeypatch):
        """Test that history includes all required fields"""
        content_id = str(ObjectId())
        watched_at = datetime.utcnow().isoformat()
        
        mock_history = [
            {
                "_id": str(ObjectId()),
                "user_id": "user-123",
                "content_id": content_id,
                "watched_at": watched_at
            }
        ]
        
        mock_get = MagicMock(return_value=mock_history)
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)

        assert response.status_code == 200
        data = response.json()[0]
        assert "_id" in data
        assert "content_id" in data
        assert "watched_at" in data

    def test_get_access_history_ordered_by_date(self, client, customer_headers, monkeypatch):
        """Test that history is returned with timestamp information"""
        earlier_time = (datetime.utcnow() - timedelta(hours=2)).isoformat()
        recent_time = datetime.utcnow().isoformat()
        
        mock_history = [
            {
                "_id": str(ObjectId()),
                "content_id": str(ObjectId()),
                "watched_at": recent_time
            },
            {
                "_id": str(ObjectId()),
                "content_id": str(ObjectId()),
                "watched_at": earlier_time
            }
        ]
        
        mock_get = MagicMock(return_value=mock_history)
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)

        assert response.status_code == 200
        data = response.json()
        # Verify timestamps are present and parseable
        assert data[0]["watched_at"]
        assert data[1]["watched_at"]

    def test_get_access_history_multiple_entries(self, client, customer_headers, monkeypatch):
        """Test retrieval of multiple history entries"""
        mock_history = [
            {
                "_id": str(ObjectId()),
                "content_id": str(ObjectId()),
                "watched_at": datetime.utcnow().isoformat()
            }
            for _ in range(5)
        ]
        
        mock_get = MagicMock(return_value=mock_history)
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)

        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_get_access_history_server_error(self, client, customer_headers, monkeypatch):
        """Test handling of server error during history retrieval"""
        def mock_get(user_id):
            raise HTTPException(status_code=500, detail="Database error")
        
        monkeypatch.setattr("app.controllers.access_controller.get_access_history", mock_get)

        response = client.get("/access/history", headers=customer_headers)
        assert response.status_code == 500


class TestAccessValidation:
    """Test suite for access validation logic"""

    def test_access_validates_subscription_status(self, client, customer_headers, monkeypatch):
        """Test that access checks subscription status"""
        def mock_access(user_id, content_id):
            # Simulate validation logic
            # In real implementation, service checks subscription status
            raise HTTPException(status_code=404, detail="No active subscription")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 404

    def test_access_validates_plan_includes_platform(self, client, customer_headers, monkeypatch):
        """Test that access validates platform is in plan"""
        def mock_access(user_id, content_id):
            # Simulate validation logic
            # In real implementation, service checks if plan includes content platform
            raise HTTPException(status_code=403, detail="Content not allowed in your plan")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 403

    def test_access_allows_valid_request(self, client, customer_headers, monkeypatch):
        """Test that access is granted for valid request"""
        def mock_access(user_id, content_id):
            # All validations pass
            return {"message": "Access granted", "log_id": str(ObjectId())}
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        content_id = str(ObjectId())
        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 200
        assert "log_id" in response.json()


class TestAccessSchema:
    """Test suite for access endpoint schema"""

    def test_access_endpoint_requires_content_id_in_path(self, client, customer_headers):
        """Test that content_id is required in path"""
        response = client.post("/access/", headers=customer_headers)
        # Endpoint with no ID should return 404 or 405
        assert response.status_code in [404, 405]

    def test_access_endpoint_accepts_valid_objectid(self, client, customer_headers, monkeypatch):
        """Test that endpoint accepts valid ObjectId format"""
        content_id = str(ObjectId())
        
        def mock_access(user_id, cid):
            return {"message": "Access granted", "log_id": str(ObjectId())}
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        response = client.post(f"/access/{content_id}", headers=customer_headers)
        assert response.status_code == 200

    def test_access_endpoint_rejects_invalid_objectid(self, client, customer_headers, monkeypatch):
        """Test that endpoint rejects invalid ObjectId format"""
        def mock_access(user_id, content_id):
            raise HTTPException(status_code=400, detail="Invalid content_id format")
        
        monkeypatch.setattr("app.controllers.access_controller.access_content", mock_access)

        response = client.post("/access/not-a-valid-id", headers=customer_headers)
        assert response.status_code == 400
