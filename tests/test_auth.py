import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException


class TestAuthRegister:
    """Test suite for user registration"""

    def test_register_customer_success(self, client, sample_user_data, monkeypatch):
        """Test successful customer registration"""
        mock_register = MagicMock(return_value={"message": "User registered successfully", "user_id": "123abc"})
        monkeypatch.setattr("app.controllers.auth_controller.register", mock_register)

        response = client.post("/auth/register", json=sample_user_data)

        assert response.status_code == 200
        assert response.json()["user_id"] == "123abc"
        mock_register.assert_called_once()

    def test_register_admin_success(self, client, sample_admin_data, monkeypatch):
        """Test successful admin registration"""
        mock_register = MagicMock(return_value={"message": "User registered successfully", "user_id": "456def"})
        monkeypatch.setattr("app.controllers.auth_controller.register", mock_register)

        response = client.post("/auth/register", json=sample_admin_data)

        assert response.status_code == 200
        assert response.json()["user_id"] == "456def"

    def test_register_missing_mobile_number(self, client):
        """Test registration fails when mobile_number is missing"""
        payload = {"password": "Test123", "role": "customer"}
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422  # Validation error

    def test_register_missing_password(self, client):
        """Test registration fails when password is missing"""
        payload = {"mobile_number": "9876543210", "role": "customer"}
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_default_role_is_customer(self, client, monkeypatch):
        """Test that registration defaults role to 'customer' if not specified"""
        payload = {"mobile_number": "9876543210", "password": "Test123"}
        
        captured_user = {}
        
        def mock_register(user):
            captured_user.update({"role": user.role, "mobile": user.mobile_number})
            return {"message": "User registered successfully", "user_id": "123"}
        
        monkeypatch.setattr("app.controllers.auth_controller.register", mock_register)
        
        response = client.post("/auth/register", json=payload)
        
        assert response.status_code == 200
        assert captured_user["role"] == "customer"

    def test_register_handles_duplicate_mobile(self, client, monkeypatch):
        """Test registration fails if mobile_number already exists"""
        def mock_register(user):
            raise HTTPException(status_code=400, detail="User already exists")
        
        monkeypatch.setattr("app.controllers.auth_controller.register", mock_register)
        
        response = client.post("/auth/register", json={"mobile_number": "9876543210", "password": "Test123", "role": "customer"})
        
        assert response.status_code == 400
        assert response.json()["detail"] == "User already exists"

    def test_register_handles_server_error(self, client, monkeypatch):
        """Test registration returns 500 on unexpected error"""
        def mock_register(user):
            raise HTTPException(status_code=500, detail="Internal server error")
        
        monkeypatch.setattr("app.controllers.auth_controller.register", mock_register)
        
        response = client.post("/auth/register", json={"mobile_number": "9876543210", "password": "Test123"})
        
        assert response.status_code == 500


class TestAuthLogin:
    """Test suite for user login"""

    def test_login_success(self, client, monkeypatch):
        """Test successful login"""
        mock_login = MagicMock(return_value={
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "token_type": "bearer"
        })
        monkeypatch.setattr("app.controllers.auth_controller.login", mock_login)

        payload = {"mobile_number": "9876543210", "password": "Test123"}
        response = client.post("/auth/login", json=payload)

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_missing_mobile_number(self, client):
        """Test login fails when mobile_number is missing"""
        payload = {"password": "Test123"}
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 422

    def test_login_missing_password(self, client):
        """Test login fails when password is missing"""
        payload = {"mobile_number": "9876543210"}
        response = client.post("/auth/login", json=payload)
        assert response.status_code == 422

    def test_login_invalid_credentials(self, client, monkeypatch):
        """Test login fails with invalid credentials"""
        def mock_login(user):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        monkeypatch.setattr("app.controllers.auth_controller.login", mock_login)

        response = client.post("/auth/login", json={"mobile_number": "9876543210", "password": "Wrong123"})

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_user_not_found(self, client, monkeypatch):
        """Test login fails when user doesn't exist"""
        def mock_login(user):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        monkeypatch.setattr("app.controllers.auth_controller.login", mock_login)

        response = client.post("/auth/login", json={"mobile_number": "9999999999", "password": "Test123"})

        assert response.status_code == 401

    def test_login_inactive_user(self, client, monkeypatch):
        """Test login fails for inactive user"""
        def mock_login(user):
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        monkeypatch.setattr("app.controllers.auth_controller.login", mock_login)

        response = client.post("/auth/login", json={"mobile_number": "9876543210", "password": "Test123"})

        assert response.status_code == 403

    def test_login_returns_valid_jwt_token(self, client, monkeypatch):
        """Test that login returns a valid JWT token"""
        from app.core.security import create_token
        
        token = create_token({"user_id": "user-123", "role": "customer"})
        
        def mock_login(user):
            return {"access_token": token, "token_type": "bearer"}
        
        monkeypatch.setattr("app.controllers.auth_controller.login", mock_login)

        response = client.post("/auth/login", json={"mobile_number": "9876543210", "password": "Test123"})

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == token
        assert data["token_type"] == "bearer"


class TestPasswordSecurity:
    """Test suite for password security"""

    def test_password_hash_length_validation(self):
        """Test that long passwords are handled safely (72 byte limit for bcrypt)"""
        from app.core.security import hash_password, verify_password
        
        long_password = "a" * 100
        hashed = hash_password(long_password)
        
        # Verify should still work after truncation
        assert verify_password(long_password, hashed)

    def test_password_verify_fails_with_wrong_password(self):
        """Test password verification fails with incorrect password"""
        from app.core.security import hash_password, verify_password
        
        password = "CorrectPassword123"
        hashed = hash_password(password)
        
        assert not verify_password("WrongPassword456", hashed)

    def test_password_multibyte_chars_handled(self):
        """Test password with multibyte characters is handled correctly"""
        from app.core.security import hash_password, verify_password
        
        password = "パスワード🔐Ñoño"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed)

    def test_json_web_token_created_with_user_data(self, admin_token):
        """Test that JWT token contains user data"""
        from pydantic import ValidationError
        from jose import jwt
        from app.core.config import SECRET_KEY
        
        payload = jwt.decode(admin_token, SECRET_KEY, algorithms=["HS256"])
        
        assert "user_id" in payload
        assert "role" in payload
        assert "exp" in payload
