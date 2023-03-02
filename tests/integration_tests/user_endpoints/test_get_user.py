from unittest.mock import patch

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_get_user(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS)

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_get_user_email_not_exists(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = None

    response = client.get(url="/users/metoonaf@gmail.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
