from tests.integration_tests.user_endpoints.utils import *


def test_login() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.post(url=f"/users/login", json={"parameter": LOGIN_REQUEST})
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User logged in successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)


def test_login_user_not_exists() -> None:
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


def test_login_incorrect_password() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.post(url=f"/users/login", json={"parameter": {**LOGIN_REQUEST, "password": "aaa"}})
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password given"}

    validate_user_deletion(USER_DETAILS)
