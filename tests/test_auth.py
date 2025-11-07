from os import wait
import time
import unittest
from base import BaseTestClass
from tests.test_data import TEST_USERS
from user.auth import (
    hash_user_password,
    check_user_password,
    get_jwt_token,
    validate_jwt_token,
)


class Testusers(BaseTestClass):
    def test_check_correct_pass(self):
        user = TEST_USERS[1]

        hashed_password = hash_user_password(user.password)

        self.assertTrue(check_user_password(user.password, hashed_password))

    def test_check_incorrect_pass(self):
        user = TEST_USERS[1]
        dummy_password = "WrongPassword"

        hashed_password = hash_user_password(user.password)

        self.assertFalse(check_user_password(dummy_password, hashed_password))

    def test_jwt_token(self):
        user = TEST_USERS[1]

        token = get_jwt_token(user.name, self.config.secret_key, 60)
        decoded = validate_jwt_token(token, self.config.secret_key)


if __name__ == "__main__":
    unittest.main()
