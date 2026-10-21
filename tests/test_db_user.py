import pytest
from sqlalchemy.orm import Session

from db.models import User
from tests.test_data import TEST_USERS
from user.auth import hash_user_password


def test_add_user(config, db):
    user = TEST_USERS[1]
    hashed_pass = hash_user_password(user.password)
    db.add_user(user.name, hashed_pass, user.is_admin)

    with Session(db.engine) as session:
        expected_user = User(user.name, hashed_pass, user.is_admin)
        added_user = session.get(User, 1)

        assert added_user is not None
        assert added_user.name == expected_user.name
        assert added_user.password == expected_user.password
        assert added_user.is_admin == expected_user.is_admin


def test_add_duplicate_user_error(config, db):
    user = TEST_USERS[1]
    hashed_pass = hash_user_password(user.password)
    db.add_user(user.name, hashed_pass, user.is_admin)

    with pytest.raises(KeyError):
        db.add_user(user.name, hashed_pass, user.is_admin)


def test_get_user(config, db):
    user = TEST_USERS[1]
    hashed_pass = hash_user_password(user.password)
    db.add_user(user.name, hashed_pass, user.is_admin)

    expected_user = User(user.name, hashed_pass, user.is_admin)
    retrieved_user = db.get_user(user.name)

    assert retrieved_user.name == expected_user.name
    assert retrieved_user.password == expected_user.password
    assert retrieved_user.is_admin == expected_user.is_admin


def test_get_user_non_existing_error(config, db):
    user = TEST_USERS[1]
    other_user = TEST_USERS[2]

    hashed_pass = hash_user_password(user.password)
    db.add_user(user.name, hashed_pass, user.is_admin)

    with pytest.raises(KeyError):
        db.get_user(other_user.name)


def test_delete_user(config, db):
    user = TEST_USERS[1]

    hashed_pass = hash_user_password(user.password)
    added_user = db.add_user(user.name, hashed_pass, user.is_admin)

    db.delete_user(added_user.id)

    with pytest.raises(KeyError):
        db.get_user(user.name)
