import pytest

from copy import deepcopy

from sqlalchemy.exc import IntegrityError

from tests.integration_tests.user_endpoints.utils import *


def test_create_user() -> None:
    validate_user_creation(user_details=USER_DETAILS)
    validate_user_deletion(user_details=USER_DETAILS)


def test_create_user_no_email() -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["email"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


def test_create_user_no_password() -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["password"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


def test_create_user_no_phone_number() -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["phone_number"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


def test_create_user_no_full_name() -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["full_name"]
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=user_details)


def test_create_user_no_car_model_no_car_color_no_plate_number() -> None:
    user_details = deepcopy(USER_DETAILS)
    del user_details["car_model"]
    del user_details["car_color"]
    del user_details["plate_number"]
    validate_user_creation(user_details=user_details)
    validate_user_deletion(user_details=user_details)


def test_create_user_user_already_exists() -> None:
    validate_user_creation(user_details=USER_DETAILS)
    with pytest.raises(IntegrityError):
        validate_user_creation(user_details=USER_DETAILS)
    validate_user_deletion(user_details=USER_DETAILS)
