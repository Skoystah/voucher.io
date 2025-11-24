from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    mapped_column,
    Mapped,
)
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime
from sqlalchemy import Boolean, CheckConstraint, String


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Voucher(Base):
    __tablename__ = "voucher"

    code: Mapped[str] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(
        String(2),
        CheckConstraint("duration in ('1h','2h','4h', '12h')", name="ck_duration"),
    )
    used: Mapped[bool] = mapped_column(
        Boolean,
        CheckConstraint("used in (0,1)", name="ck_voucher_used"),
        default=False,
        server_default="0",
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        CheckConstraint("is_admin in (0,1)", name="ck_user_is_admin"),
        default=False,
        server_default="0",
    )
    last_login: Mapped[DateTime] = mapped_column(
        DateTime, default=now(), server_default=now()
    )
