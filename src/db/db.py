from typing import List
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db.models import Base, Voucher, User


class DB:
    def __init__(
        self,
        db_url: str = "voucher.db",
        db_auth_token: str | None = None,
        verbose: bool | None = False,
    ):
        # TODO more elegant way to decide between local and remote?
        if db_auth_token:
            # For now chosen remote only DB - can also be changed to embedded (local copy + remote)
            self.engine = create_engine(
                f"sqlite+{db_url}?secure=true",
                connect_args={
                    "auth_token": db_auth_token,
                },
                echo=verbose,
            )
        else:
            self.engine = create_engine(f"sqlite+libsql:///{db_url}", echo=verbose)

        Base.metadata.create_all(self.engine)

    def add_voucher(self, code: str, duration: str) -> Voucher:
        with Session(self.engine, expire_on_commit=False) as session:
            try:
                added_voucher = Voucher(code, duration)
                session.add(added_voucher)
                session.commit()

                if added_voucher:
                    return added_voucher
                else:
                    raise ValueError("Voucher could not be added")
            # TODO _ better way? SQLite returns IntegrityError while Turso returns ValueError!
            except (IntegrityError, ValueError):
                session.rollback()
                raise KeyError("Voucher already exists")

    def get_voucher(self, code: str) -> Voucher:
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")

            return voucher

    def get_vouchers(
        self, duration: str | None = None, used: bool | None = None
    ) -> List[Voucher]:
        filters = {}
        if duration:
            filters["duration"] = duration
        if used is not None:
            filters["used"] = used

        with Session(self.engine) as session:
            vouchers = session.scalars(select(Voucher).filter_by(**filters))
            return list(vouchers)

    def use_voucher(self, code: str) -> Voucher:
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")

            if voucher.used:
                raise ValueError("Voucher was already used")

            voucher.used = True
            session.commit()

            return voucher

    def delete_voucher(self, code: str) -> None:
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")
            session.delete(voucher)
            session.commit()

    def add_user(self, name: str, password: str, is_admin: bool) -> User:
        with Session(self.engine, expire_on_commit=False) as session:
            try:
                added_user = User(name=name, password=password, is_admin=is_admin)
                session.add(added_user)
                session.commit()

                if added_user:
                    return added_user
                else:
                    raise ValueError("User could not be added")
            # TODO _ better way? SQLite returns IntegrityError while Turso returns ValueError!
            except (IntegrityError, ValueError):
                session.rollback()
                raise KeyError("User already exists")

    def get_user(self, name: str) -> User:
        with Session(self.engine) as session:
            user = session.scalar(select(User).filter_by(name=name))
            if user is None:
                raise KeyError("User does not exist")

            return user

    def update_user(self, id: int, password: str) -> None:
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user is None:
                raise KeyError("User does not exist")

            user.password = password
            session.commit()

            return

    def delete_user(self, id: int) -> None:
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user is None:
                raise KeyError("User does not exist")
            session.delete(user)
            session.commit()
