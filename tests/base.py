import unittest
from config import Config
from voucher.db import DB
import os

class BaseTestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(db="test_voucher.db")
        self.db = DB("test_voucher.db")
        with open("sql/create_db_001","r") as f:
            self.db.connection.executescript(f.read())

    def tearDown(self) -> None:
        self.db.connection.close()
        os.remove("test_voucher.db")
