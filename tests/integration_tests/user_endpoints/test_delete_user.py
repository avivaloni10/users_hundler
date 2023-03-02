from unittest.mock import patch

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(DELETE_USER_BY_EMAIL_IMPORT_PATH)
@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_delete_user(get_user_by_email_mock, delete_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS)
    delete_user_by_email_mock.return_value = None

    validate_user_deletion(USER_DETAILS)


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_delete_user_user_not_exists(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = None

    validate_user_deletion(USER_DETAILS, expected_status_code=404, expected_result={"detail": "User not found"})
