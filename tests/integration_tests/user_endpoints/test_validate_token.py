from unittest.mock import patch

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(GET_USER_BY_TOKEN_IMPORT_PATH)
def test_validate_token(get_user_by_token_mock) -> None:
    get_user_by_token_mock.return_value = User(**USER_DETAILS)

    response = client.get(url="/users/validate_token", headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == 200
    assert response.json() == {
        'code': 200,
        'message': 'Token is valid',
        'result': {"is_valid": True},
        'status': 'OK'
    }


@patch(GET_USER_BY_TOKEN_IMPORT_PATH)
def test_validate_token_not_exists(get_user_by_token_mock) -> None:
    get_user_by_token_mock.return_value = None

    response = client.get(url="/users/validate_token", headers={
        'Authorization': f'Bearer f7948d51-613c-5301-9d98-a741bbb7f8ed'
    })
    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized'}
