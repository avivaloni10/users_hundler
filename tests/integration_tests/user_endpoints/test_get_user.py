from tests.integration_tests.user_endpoints.utils import *


def test_get_user() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)


def test_get_user_email_not_exists() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.get(url="/users/metoonaf@gmail.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

    validate_user_deletion(USER_DETAILS)
