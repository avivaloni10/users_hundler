from tests.integration_tests.user_endpoints.utils import *


def test_delete_user() -> None:
    validate_user_creation(USER_DETAILS)
    validate_user_deletion(USER_DETAILS)


def test_delete_user_user_not_exists() -> None:
    validate_user_deletion(USER_DETAILS, expected_status_code=404, expected_result={"detail": "User not found"})
