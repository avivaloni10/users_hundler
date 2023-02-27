from copy import deepcopy

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

USER_DETAILS = {'car_color': 'Black',
                'car_model': 'Hatzil',
                'email': 'a@gmail.com',
                'full_name': 'Dov Sherman',
                'password': 'Aa111111',
                'phone_number': '0541112222',
                'plate_number': '0000000'}

UPDATED_USER_DETAILS = {'plate_number': '1111111'}


def test_create_user_delete_user():
    validate_user_creation()
    validate_user_deletion()


def test_get_users():
    validate_user_creation()

    response = client.get(url="/users")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'Users batch fetched successfully',
        'result': [USER_DETAILS],
        'status': 'OK'
    }

    validate_user_deletion()


def test_get_user():
    validate_user_creation()

    response = client.get(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'User fetched successfully',
        'result': USER_DETAILS,
        'status': 'OK'
    }

    validate_user_deletion()


def test_update_user():
    validate_user_creation()

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

    validate_user_deletion()


def validate_user_creation():
    response = client.post(url="/users", json={"parameter": USER_DETAILS})
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'User created successfully', 'status': 'OK'}


def validate_user_deletion():
    response = client.delete(url=f"/users/{USER_DETAILS['email']}")
    assert response.status_code == 200
    assert response.json() == {'code': 200, 'message': 'User deleted successfully', 'status': 'OK'}
