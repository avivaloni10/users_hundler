from unittest.mock import patch

import pytest

from copy import deepcopy

from models.user import User
from tests.integration_tests.user_endpoints.utils import *


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user(create_user_mock) -> None:
    create_user_mock.return_value = User(**USER_DETAILS)

    validate_user_creation(user_details=USER_DETAILS)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_no_email(create_user_mock) -> None:
    create_user_mock.side_effect = IntegrityError(None, None, None)

    user_details = deepcopy(USER_DETAILS)
    del user_details["email"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_no_password(create_user_mock) -> None:
    create_user_mock.side_effect = IntegrityError(None, None, None)

    user_details = deepcopy(USER_DETAILS)
    del user_details["password"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_no_phone_number(create_user_mock) -> None:
    create_user_mock.side_effect = IntegrityError(None, None, None)

    user_details = deepcopy(USER_DETAILS)
    del user_details["phone_number"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_no_full_name(create_user_mock) -> None:
    create_user_mock.side_effect = IntegrityError(None, None, None)

    user_details = deepcopy(USER_DETAILS)
    del user_details["full_name"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_no_car_model_no_car_color_no_plate_number(create_user_mock) -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["car_model"]
    del user_details["car_color"]
    del user_details["plate_number"]

    create_user_mock.return_value = User(**user_details)

    validate_user_creation(user_details=user_details)


@patch(CREATE_USER_IMPORT_PATH)
def test_create_user_user_already_exists(create_user_mock) -> None:
    create_user_mock.side_effect = [User(**USER_DETAILS), IntegrityError(None, None, None)]

    validate_user_creation(user_details=USER_DETAILS)
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=USER_DETAILS)
