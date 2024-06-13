import pytest
import os
from api.post_sign_up import SignUp
from dotenv import load_dotenv
import requests

load_dotenv()

@pytest.fixture
def sign_up_api():
    return SignUp()

def test_successful_api_signup(sign_up_api: SignUp):
    response = sign_up_api.api_call("newuser", "validpassword123", "newuser@example.com")
    try:
        response.raise_for_status()
        assert response.status_code == 200, "Expected status code 200"
        assert response.json()['token'] is not None, "Token should not be None"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")

def test_should_return_400_if_username_or_password_too_short(sign_up_api: SignUp):
    try:
        sign_up_api.api_call("us", "pw", "short@example.com")
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "username length" in e.response.json()["username"], "Username error should mention length"
        assert "password length" in e.response.json()["password"], "Password error should mention length"

def test_should_return_422_on_existing_user(sign_up_api: SignUp):
    try:
        sign_up_api.api_call(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"), "existinguser@example.com")
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422"
        assert "User already exists" == e.response.json()["message"], "Expected error message for existing user"

def test_should_return_500_on_server_error(sign_up_api: SignUp):
    try:
        # Simulate a condition that would cause a server error
        sign_up_api.api_call("newuser", "validpassword123", "servererror@example.com")
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 500, "Expected status code 500"
        pytest.fail(f"Server error occurred: {str(e)}")

