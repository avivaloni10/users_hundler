from tests.integration_tests.user_endpoints.utils import *


def test_create_user_delete_user() -> None:
    validate_user_creation(USER_DETAILS)
    validate_user_deletion(USER_DETAILS)


def test_get_users() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.get(url="/users")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'Users batch fetched successfully',
        'result': [USER_DETAILS],
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)


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


def test_update_user() -> None:
    validate_user_creation(USER_DETAILS)

    response = client.put(url=f"/users/{USER_DETAILS['email']}", json={"parameter": UPDATED_USER_DETAILS})
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'User updated successfully', 'status': 'OK'}

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': {**USER_DETAILS, **UPDATED_USER_DETAILS},
        'status': 'OK'
    }

    validate_user_deletion(USER_DETAILS)
