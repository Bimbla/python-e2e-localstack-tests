import pytest
import requests
from api.post_sign_up import SignUp
from api.delete_user import DeleteUser
from api.post_sign_in import SignIn
from api.data.register import RegisterRequestDto

def test_successful_sign_up(sign_up_api: SignUp, delete_user_api: DeleteUser, sign_in_api: SignIn, user_credentials: RegisterRequestDto):
    sign_up_response = sign_up_api.api_call(user_credentials)
    token = sign_up_response.json().get('token')
    assert token is not None, "Token should not be None"
    assert sign_up_response.status_code == 201, f"Expected status code 201, code: {sign_up_response.status_code}"

    # Sign in the user
    sign_in_response = sign_in_api.api_call(user_credentials.username, user_credentials.password)
    token = sign_in_response.json().get('token')

    # Delete the user after the test is done
    delete_user_api.api_call(user_credentials.username, token)


def test_invalid_username_integer(sign_up_api: SignUp, user_credentials: RegisterRequestDto):
    user_credentials.username = 123
    try:
        response = sign_up_api.api_call(user_credentials)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid username, code: {e.response.status_code}"
        assert "Field validation failed" in e.response.text, f"Expected error message for invalid username in {e.response.text}"


def test_invalid_password_single_letter(sign_up_api: SignUp, user_credentials: RegisterRequestDto):
    user_credentials.password = "a"
    try:
        response = sign_up_api.api_call(user_credentials)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid password, code: {e.response.status_code}"
        assert "Minimum password length: 4 characters" in e.response.text, f"Expected error message for invalid password in {e.response.text}"


def test_invalid_roles_nonexistent(sign_up_api: SignUp, user_credentials: RegisterRequestDto):
    user_credentials.roles = ["ROLE_NONEXISTENT"]
    try:
        response = sign_up_api.api_call(user_credentials)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid role, code: {e.response.status_code}"
        assert "Field validation failed" in e.response.text, f"Expected error message for invalid role in {e.response.text}"


def test_invalid_email_no_at_sign(sign_up_api: SignUp, user_credentials: RegisterRequestDto):
    user_credentials.email = "invalidemail.com"
    try:
        response = sign_up_api.api_call(user_credentials)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid email, code: {e.response.status_code}"
        assert "Field validation failed" in e.response.text, f"Expected error message for invalid email in {e.response.text}"


def test_internal_server_error(sign_up_api: SignUp, user_credentials: RegisterRequestDto):
    user_credentials.username = "trigger500error"
    try:
        response = sign_up_api.api_call(user_credentials)
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 500, f"Expected status code 500 for server error, code: {e.response.status_code}"
        assert "Internal Server Error" in e.response.text, f"Expected error message for server error in {e.response.text}"
