import os
from pathlib import Path

import pytest

from config import Config
from db.db import DB

TEST_DB_FILE = "test_voucher.db"


@pytest.fixture
def config():
    """A fresh application config backed by its own SQLite file.

    The database file is unique per test, so tests cannot see each other's
    rows, and it is removed afterwards even if the test failed.
    """
    secret_key = os.getenv("SECRET", "dummy")
    test_config = Config(DB(TEST_DB_FILE, verbose=False), secret_key=secret_key)
    yield test_config
    # A test that errored before touching the DB leaves no file behind.
    for suffix in ("", "-wal", "-shm"):
        Path(f"{TEST_DB_FILE}{suffix}").unlink(missing_ok=True)


@pytest.fixture
def db(config):
    return config.db
