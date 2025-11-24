from db.db import DB


class Config:
    def __init__(self, db: DB, secret_key: str):
        self.db = db
        self.secret_key = secret_key
