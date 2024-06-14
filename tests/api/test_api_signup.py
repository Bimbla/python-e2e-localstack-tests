import logging

import pytest
import requests
from api.post_sign_up import SignUp
from generators.user_generator import get_random_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def sign_up_api():
    return SignUp()

def test_successful_api_signup(sign_up_api: SignUp):
    user = get_random_user()
    response = sign_up_api.api_call(user)
    try:
        response.raise_for_status()
        assert response.status_code == 201, "Expected status code 201"
        assert response.json()['token'] is not None, "Token should not be None"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTPError occurred: {str(e)}")

def test_should_return_400_if_username_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.username = "abc"  # intentionally short username
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "username length" in e.response.json()["username"], "Username error"

def test_should_return_400_if_email_invalid(sign_up_api: SignUp):
    user = get_random_user()
    user.email = "not-an-email"  # intentionally invalid email
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
            "must be a well-formed email address" in e.response.json()["email"]
        ), "Email error should mention being a well-formed email address"

def test_should_return_400_if_username_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.username = "abc"  # intentionally short username
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "username length" in e.response.json()["username"], "Username error"
        assert "Minimum username length: 4 characters" in e.response.json()["username"], "Username error"

def test_should_return_400_if_role_invalid(sign_up_api: SignUp):
    user = get_random_user()
    user.roles = ["ROLE_CLIENT"]  # intentionally invalid role
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "invalid role" in e.response.json()["roles"], "Role error"


def test_should_return_400_if_role_invalid(sign_up_api: SignUp):
    user = get_random_user()
    user.roles = ["ROLE_CLIENT"]  # intentionally invalid role
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "Invalid role" in e.response.json()["roles"], "Role error"

def test_should_return_400_if_first_name_missing(sign_up_api: SignUp):
    user = get_random_user()
    user.firstName = ""  # intentionally missing first name
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "Minimum firstName length" in e.response.json()["firstName"], "First name error"

def test_should_return_400_if_last_name_missing(sign_up_api: SignUp):
    user = get_random_user()
    user.lastName = ""  # intentionally missing last name
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"


def test_should_return_400_if_password_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.password = "123"  # intentionally short password
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert "Minimum password length: 8 characters" in e.response.json()["password"], "Password error"

def test_should_return_400_if_password_too_short_2(sign_up_api: SignUp):
    user = get_random_user()
    user.password = "123"  # intentionally short password
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        response_json = e.response.json()
        logger.error(f"Response JSON: {response_json}")
        assert e.response.status_code == 400, "Expected status code 400"
        assert "Minimum password length: 4 characters" in response_json["password"], "Password error"