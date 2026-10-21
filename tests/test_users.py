import pytest

from user.auth import hash_user_password
from user.models import UserDB


def test_add_user(config, db):
    user_name = "Jos"
    user_is_admin = True
    user_password = hash_user_password("SafePassword1")

    userDB = UserDB(config)

    userDB.add_user(user_name, user_password, user_is_admin)
    retrieved_user = db.get_user(user_name)

    assert retrieved_user.name == user_name
    assert retrieved_user.password == user_password
    assert retrieved_user.is_admin == user_is_admin


def test_add_existing_user_error(config, db):
    user_name = "Jos"
    user_is_admin = True
    user_password = hash_user_password("SafePassword1")

    userDB = UserDB(config)

    userDB.add_user(user_name, user_password, user_is_admin)

    with pytest.raises(KeyError):
        db.add_user(user_name, user_password, user_is_admin)


def test_get_user(config, db):
    user_name = "Jos"
    user_is_admin = True
    user_password = hash_user_password("SafePassword1")

    userDB = UserDB(config)

    added_user = db.add_user(user_name, user_password, user_is_admin)

    assert userDB.get_user(user_name) == added_user


def test_get_user_not_found_error(config, db):
    user_name = "Jos"
    user_is_admin = True
    user_password = hash_user_password("SafePassword1")

    other_user_name = "Francine"

    userDB = UserDB(config)

    db.add_user(user_name, user_password, user_is_admin)

    with pytest.raises(KeyError):
        userDB.get_user(other_user_name)


def test_delete_user(config, db):
    user_name = "Jos"
    user_is_admin = True
    user_password = hash_user_password("SafePassword1")

    userDB = UserDB(config)

    added_user = db.add_user(user_name, user_password, user_is_admin)

    userDB.delete_user(added_user.id)

    with pytest.raises(KeyError):
        db.get_user(user_name)
