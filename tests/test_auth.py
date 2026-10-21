from tests.test_data import TEST_USERS
from user.auth import (
    check_user_password,
    get_jwt_token,
    hash_user_password,
    validate_jwt_token,
)


def test_check_correct_pass():
    user = TEST_USERS[1]

    hashed_password = hash_user_password(user.password)

    assert check_user_password(user.password, hashed_password)


def test_check_incorrect_pass():
    user = TEST_USERS[1]
    dummy_password = "WrongPassword"

    hashed_password = hash_user_password(user.password)

    assert not check_user_password(dummy_password, hashed_password)


def test_jwt_token(config):
    user = TEST_USERS[1]

    token = get_jwt_token(user.name, config.secret_key, 60)
    _ = validate_jwt_token(token, config.secret_key)
