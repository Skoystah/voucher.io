from config import Config
from db.models import User


class UserDB:
    def __init__(self, config: Config):
        self.db = config.db

    def add_user(self, name: str, password: str, is_admin: bool = False) -> User:
        return self.db.add_user(name, password, is_admin)

    def get_user(self, name: str) -> User:
        return self.db.get_user(name)

    def update_user(self, id: int, password: str) -> None:
        self.db.update_user(id, password)

    def delete_user(self, id: int) -> None:
        self.db.delete_user(id)
