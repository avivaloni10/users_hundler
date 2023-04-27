from typing import Dict, Optional

from sqlalchemy.exc import IntegrityError
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

CREATE_USER_IMPORT_PATH = "dal.user.create_user"
GET_USER_BY_EMAIL_IMPORT_PATH = "dal.user.get_user_by_email"
GET_USER_BY_TOKEN_IMPORT_PATH = "dal.user.get_user_by_token"
GET_USERS_IMPORT_PATH = "dal.user.get_users"
UPDATE_USER_BY_EMAIL_IMPORT_PATH = "dal.user.update_user_by_email"
DELETE_USER_BY_EMAIL_IMPORT_PATH = "dal.user.delete_user_by_email"

USER_DETAILS = {
    'car_color': 'Black',
    'car_model': 'Hatzil',
    'email': 'a@gmail.com',
    'full_name': 'Dov Sherman',
    'password': 'Aa111111',
    'phone_number': '0541112222',
    'plate_number': '0000000'
}

UPDATED_USER_PLATE_NUMBER = {'plate_number': '1111111'}

UPDATED_USER_EMAIL_PASSWORD_PHONE_NUMBER = {
    'email': 'b@gmail.com',
    'password': 'Bb222222',
    'phone_number': '0542223333'
}

LOGIN_REQUEST = {
    'email': 'a@gmail.com',
    'password': 'Aa111111',
}


def validate_user_creation(user_details: Dict, expected_status_code: int = 200, expected_result: Optional[Dict] = None):
    if expected_result is None:
        expected_result = {'code': 200, 'message': 'User created successfully', 'status': 'OK'}
    response = client.post(url="/users", json={"parameter": user_details})
    assert response.status_code == expected_status_code
    assert response.json() == expected_result


def validate_user_deletion(user_details: Dict, expected_status_code: int = 200, expected_result: Optional[Dict] = None):
    if expected_result is None:
        expected_result = {'code': 200, 'message': 'User deleted successfully', 'status': 'OK'}
    response = client.delete(url=f"/users/{user_details['email']}", headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == expected_status_code
    assert response.json() == expected_result
