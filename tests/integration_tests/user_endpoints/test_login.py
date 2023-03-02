from unittest.mock import patch

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS)

    response = client.post(url=f"/users/login", json={"parameter": LOGIN_REQUEST})
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User logged in successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login_user_not_exists(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = None

    response = client.post(url=f"/users/login", json={"parameter": LOGIN_REQUEST})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_login_no_email() -> None:
    response = client.post(url=f"/users/login", json={"parameter": {"password": "aaa"}})
    assert response.status_code == 400
    assert response.json() == {"detail": "Please specify email and password"}


def test_login_no_password() -> None:
    response = client.post(url=f"/users/login", json={"parameter": {"email": "a@gmail.com"}})
    assert response.status_code == 400
    assert response.json() == {"detail": "Please specify email and password"}


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login_incorrect_password(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**{**USER_DETAILS, "password": "wrong"})

    response = client.post(url=f"/users/login", json={"parameter": {**LOGIN_REQUEST, "password": "aaa"}})
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password given"}
