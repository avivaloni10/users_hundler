from tests.integration_tests.user_endpoints.utils import *


def test_update_user() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={"parameter": UPDATED_USER_PLATE_NUMBER})
    assert response.status_code == 200
    assert response.json() == {'code': 200,
                               'message': 'User updated successfully',
                               'result': {**USER_DETAILS, **UPDATED_USER_PLATE_NUMBER},
                               'status': 'OK'}

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': {**USER_DETAILS, **UPDATED_USER_PLATE_NUMBER},
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)


def test_update_user_user_not_exists() -> None:
    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={"parameter": UPDATED_USER_PLATE_NUMBER})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_not_update_email_password_phone_number() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.put(url=f"/users/{USER_DETAILS['email']}",
                          json={"parameter": UPDATED_USER_EMAIL_PASSWORD_PHONE_NUMBER})
    assert response.status_code == 200
    assert response.json() == {'code': 200,
                               'message': 'User updated successfully',
                               'result': USER_DETAILS,
                               'status': 'OK'}

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)
