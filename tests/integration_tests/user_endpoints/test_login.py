from unittest.mock import patch

import jwt

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS_ENCRYPTED_PASS)

    response = client.post(url=f"/users/token", data={
        'username': LOGIN_REQUEST['email'],
        'password': LOGIN_REQUEST['password']
    })
    assert response.status_code == 200
    assert jwt.decode(response.json()["access_token"], get_secret_key(), algorithms=['HS256'])["email"] == LOGIN_REQUEST['email']
    assert response.json()["token_type"] == 'bearer'


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login_user_not_exists(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = None

    response = client.post(url=f"/users/token", data={
        'username': LOGIN_REQUEST['email'],
        'password': LOGIN_REQUEST['password']
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong email or password given"}


def test_login_no_email() -> None:
    response = client.post(url=f"/users/token", data={'password': 'aaa'})
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'username'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


def test_login_no_password() -> None:
    response = client.post(url=f"/users/token", data={'username': LOGIN_REQUEST['email']})
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'password'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


@patch(GET_USER_BY_EMAIL_IMPORT_PATH)
def test_login_incorrect_password(get_user_by_email_mock) -> None:
    get_user_by_email_mock.return_value = User(**USER_DETAILS_ENCRYPTED_PASS)

    response = client.post(url=f"/users/token", data={'username': LOGIN_REQUEST['email'], 'password': 'aaa'})
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong email or password given"}
