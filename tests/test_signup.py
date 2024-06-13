import pytest
from api.base_api import BaseAPI

class TestSignupAPI:
    @pytest.fixture(scope='class')
    def api(self):
        return BaseAPI()

    def test_signup_success(self, api):
        payload = {
            "username": "testuser",
            "password": "securepassword",
            "email": "testuser@example.com"
        }
        response = api.make_request("POST", "users/signup", json=payload)
        assert response.status_code == 200
        assert response.json().get("message") == "User created successfully"

    def test_signup_bad_request(self, api):
        payload = {
            "username": "",  # Invalid username
            "password": "securepassword",
            "email": "testuser@example.com"
        }
        response = api.make_request("POST", "users/signup", json=payload)
        assert response.status_code == 400

    def test_signup_unprocessable_entity(self, api):
        payload = {
            "username": "testuser",
            "password": "short",  # Invalid password
            "email": "testuser@example.com"
        }
        response = api.make_request("POST", "users/signup", json=payload)
        assert response.status_code == 422

    def test_signup_server_error(self, api):
        payload = {
            "username": "erroruser",
            "password": "securepassword",
            "email": "erroruser@example.com"
        }
        response = api.make_request("POST", "users/signup", json=payload)
        assert response.status_code == 500  # This is expected to fail
