import unittest
from base import BaseTestClass
from user.models import UserDB
from user.auth import hash_user_password


class Testusers(BaseTestClass):
    def test_add_user(self):
        user_name = "Jos"
        user_is_admin = True
        user_password = hash_user_password("SafePassword1")

        userDB = UserDB(self.config)

        userDB.add_user(user_name, user_password, user_is_admin)
        retrieved_user = self.db.get_user(user_name)

        self.assertEqual(retrieved_user.name, user_name)
        self.assertEqual(retrieved_user.password, user_password)
        self.assertEqual(retrieved_user.is_admin, user_is_admin)

    def test_add_existing_user_error(self):
        user_name = "Jos"
        user_is_admin = True
        user_password = hash_user_password("SafePassword1")

        userDB = UserDB(self.config)

        userDB.add_user(user_name, user_password, user_is_admin)

        with self.assertRaises(KeyError):
            self.db.add_user(user_name, user_password, user_is_admin)

    def test_get_user(self):
        user_name = "Jos"
        user_is_admin = True
        user_password = hash_user_password("SafePassword1")

        userDB = UserDB(self.config)

        added_user = self.db.add_user(user_name, user_password, user_is_admin)

        self.assertEqual(userDB.get_user(user_name), added_user)

    def test_get_user_not_found_error(self):
        user_name = "Jos"
        user_is_admin = True
        user_password = hash_user_password("SafePassword1")

        other_user_name = "Francine"

        userDB = UserDB(self.config)

        self.db.add_user(user_name, user_password, user_is_admin)

        with self.assertRaises(KeyError):
            userDB.get_user(other_user_name)

    def test_delete_user(self):
        user_name = "Jos"
        user_is_admin = True
        user_password = hash_user_password("SafePassword1")

        userDB = UserDB(self.config)

        added_user = self.db.add_user(user_name, user_password, user_is_admin)

        userDB.delete_user(added_user.id)

        with self.assertRaises(KeyError):
            self.db.get_user(user_name)


if __name__ == "__main__":
    unittest.main()
