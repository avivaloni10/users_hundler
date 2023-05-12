from unittest.mock import patch

import jwt

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(GET_USER_BY_TOKEN_IMPORT_PATH)
def test_validate_token(get_user_by_token_mock) -> None:
    get_user_by_token_mock.return_value = User(**USER_DETAILS)

    response = client.get(url="/users/validate_token", headers={
        'Authorization': f'Bearer {token(USER_DETAILS["email"])}'
    })
    assert response.status_code == 200
    resp_json = response.json()
    del resp_json["result"]["token"]
    assert resp_json == {
        'code': 200,
        'message': 'Token is valid',
        'result': {"is_valid": True},
        'status': 'OK'
    }


def test_validate_token_not_exists() -> None:
    response = client.get(url="/users/validate_token", headers={
        'Authorization': f'Bearer aaa'
    })
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid JWT token'}
