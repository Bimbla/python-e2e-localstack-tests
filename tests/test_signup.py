import pytest
import logging
from api.base_api import BaseAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSignupAPI:
    @pytest.fixture(scope='class')
    def api(self):
        return BaseAPI()

    def test_signup_success(self, api):
        logger.info("Starting test: test_signup_success")
        payload = {
            "username": "testuser",
            "password": "securepassword",
            "email": "testuser@example.com"
        }
        try:
            response = api.make_request("POST", "users/signup", json=payload)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response body: {response.json()}")
            assert response.status_code == 200
            assert response.json().get("message") == "User created successfully"
        except Exception as e:
            logger.error(f"Error during test_signup_success: {e}")
            raise

    def test_signup_bad_request(self, api):
        logger.info("Starting test: test_signup_bad_request")
        payload = {
            "username": "",  # Invalid username
            "password": "securepassword",
            "email": "testuser@example.com"
        }
        try:
            response = api.make_request("POST", "users/signup", json=payload)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response body: {response.json()}")
            assert response.status_code == 400
        except Exception as e:
            logger.error(f"Error during test_signup_bad_request: {e}")
            raise

    def test_signup_unprocessable_entity(self, api):
        logger.info("Starting test: test_signup_unprocessable_entity")
        payload = {
            "username": "testuser",
            "password": "short",  # Invalid password
            "email": "testuser@example.com"
        }
        try:
            response = api.make_request("POST", "users/signup", json=payload)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response body: {response.json()}")
            assert response.status_code == 422
        except Exception as e:
            logger.error(f"Error during test_signup_unprocessable_entity: {e}")
            raise

    def test_signup_server_error(self, api):
        logger.info("Starting test: test_signup_server_error")
        payload = {
            "username": "erroruser",
            "password": "securepassword",
            "email": "erroruser@example.com"
        }
        try:
            response = api.make_request("POST", "users/signup", json=payload)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response body: {response.json()}")
            assert response.status_code == 500  # This is expected to fail
        except Exception as e:
            logger.error(f"Error during test_signup_server_error: {e}")
            raise
