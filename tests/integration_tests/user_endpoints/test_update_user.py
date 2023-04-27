from unittest.mock import patch

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(UPDATE_USER_BY_EMAIL_IMPORT_PATH)
@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_update_user(get_user_by_email_mock, update_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS)
    update_user_by_email_mock.return_value = User(**{**USER_DETAILS, **UPDATED_USER_PLATE_NUMBER})

    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={
        "parameter": UPDATED_USER_PLATE_NUMBER
    }, headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User updated successfully',
        'result': {**USER_DETAILS, **UPDATED_USER_PLATE_NUMBER},
        'status': 'OK'
    }


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_update_user_user_not_exists(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = None

    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={
        "parameter": UPDATED_USER_PLATE_NUMBER
    }, headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@patch(UPDATE_USER_BY_EMAIL_IMPORT_PATH)
@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_update_user_not_update_email_password_phone_number(get_user_by_email_mock, update_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS)
    update_user_by_email_mock.return_value = User(**USER_DETAILS)

    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={
        "parameter": UPDATED_USER_EMAIL_PASSWORD_PHONE_NUMBER
    }, headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User updated successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }
