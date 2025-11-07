import unittest
from config import Config
from db.db import DB
import os


class BaseTestClass(unittest.TestCase):
    def setUp(self) -> None:
        secret_key = os.getenv("SECRET")
        if secret_key is None:
            secret_key = "dummy"

        self.config = Config(
            DB("test_voucher.db", verbose=False), secret_key=secret_key
        )
        self.db = self.config.db

    def tearDown(self) -> None:
        os.remove("test_voucher.db")
