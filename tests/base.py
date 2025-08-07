import unittest
from config import Config
from voucher.db import DB
import os

class BaseTestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(DB("test_voucher.db", verbose=False))
        self.db = self.config.db

    def tearDown(self) -> None:
        # self.db.engine.dispose()
        os.remove("test_voucher.db")
