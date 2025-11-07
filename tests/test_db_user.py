import unittest
from base import BaseTestClass
from tests.test_data import TEST_USERS
from db.models import User
from sqlalchemy.orm import Session
from user.auth import hash_user_password


class TestDB(BaseTestClass):
    def test_add_user(self):
        user = TEST_USERS[1]
        hashed_pass = hash_user_password(user.password)
        self.db.add_user(user.name, hashed_pass, user.is_admin)

        with Session(self.db.engine) as session:
            expected_user = User(user.name, hashed_pass, user.is_admin)
            added_user = session.get(User, 1)

            self.assertIsNotNone(added_user)

            if added_user:
                self.assertEqual(added_user.name, expected_user.name)
                self.assertEqual(added_user.password, expected_user.password)
                self.assertEqual(added_user.is_admin, expected_user.is_admin)

    def test_add_duplicate_user_error(self):
        user = TEST_USERS[1]
        hashed_pass = hash_user_password(user.password)
        self.db.add_user(user.name, hashed_pass, user.is_admin)

        with self.assertRaises(KeyError):
            self.db.add_user(user.name, hashed_pass, user.is_admin)

    def test_get_user(self):
        user = TEST_USERS[1]
        hashed_pass = hash_user_password(user.password)
        self.db.add_user(user.name, hashed_pass, user.is_admin)

        expected_user = User(user.name, hashed_pass, user.is_admin)
        retrieved_user = self.db.get_user(user.name)

        self.assertEqual(retrieved_user.name, expected_user.name)
        self.assertEqual(retrieved_user.password, expected_user.password)
        self.assertEqual(retrieved_user.is_admin, expected_user.is_admin)

    def test_get_user_non_existing_error(self):
        user = TEST_USERS[1]
        other_user = TEST_USERS[2]

        hashed_pass = hash_user_password(user.password)
        self.db.add_user(user.name, hashed_pass, user.is_admin)

        with self.assertRaises(KeyError):
            self.db.get_user(other_user.name)

    def test_delete_voucher(self):
        user = TEST_USERS[1]

        hashed_pass = hash_user_password(user.password)
        added_user = self.db.add_user(user.name, hashed_pass, user.is_admin)

        self.db.delete_user(added_user.id)

        with self.assertRaises(KeyError):
            self.db.get_user(user.name)


if __name__ == "__main__":
    unittest.main()
