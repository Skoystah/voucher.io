import unittest
from config import Config
import voucher.db as db
import os

class BaseTestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(db="test_voucher.db", verbose=False)
        self.db = db.DB("test_voucher.db", verbose=False)

    def tearDown(self) -> None:
        # self.db.engine.dispose()
        os.remove("test_voucher.db")
