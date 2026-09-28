from db.db import DB


class Config:
    def __init__(self, db: DB, secret_key: str, auth_disabled: bool = False):
        self.db = db
        self.secret_key = secret_key
        self.auth_disabled = auth_disabled
