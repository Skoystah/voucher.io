from typing import List
from sqlalchemy import Boolean, CheckConstraint, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session, mapped_column, Mapped

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Voucher(Base):
    __tablename__ = "voucher"

    code: Mapped[str] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(2), 
                                          CheckConstraint("duration in ('1h','2h','4h', '12h')", 
                                                          name="ck_duration"))
    used: Mapped[bool] = mapped_column(Boolean, 
                                       CheckConstraint("used in (0,1)", 
                                                       name="ck_voucher_used"), 
                                       default=False)
    

class DB():
    def __init__(self, 
                 db_url: str ="voucher.db", 
                 db_auth_token: str | None = None, 
                 verbose: bool | None =True):

        # TODO more elegant way to decide between local and remote?
        if db_auth_token:
            # For now chosen remote only DB - can also be changed to embedded (local copy + remote)
            self.engine = create_engine(
                    f'sqlite+{db_url}?secure=true',
                    connect_args={
                            "auth_token" : db_auth_token,
                            },
                    echo=verbose,
                    )
        else:
            self.engine = create_engine(
                    f'sqlite+libsql:///{db_url}', 
                    echo=verbose
                    )

        Base.metadata.create_all(self.engine) 

    def add_voucher(self, 
                    code: str,
                    duration: str) -> Voucher:

        with Session(self.engine) as session:
            try:
                session.add(Voucher(code, duration))
                session.commit()

                added_voucher =  session.get(Voucher, code)
                if added_voucher:
                    return added_voucher
                else:
                    raise ValueError("Voucher could not be added")
            # TODO _ better way? SQLite returns IntegrityError while Turso returns ValueError!
            except (IntegrityError, ValueError):
                session.rollback()
                raise KeyError("Voucher already exists")
            

    def get_voucher(self, 
                    code: str) -> Voucher:

        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")
            
            return voucher

    def get_vouchers(self, 
                     duration: str | None = None, 
                     used: bool | None = None) -> List[Voucher]:

        filters = {}
        if duration:
            filters['duration'] = duration
        if used is not None:
            filters['used'] = used

        with Session(self.engine) as session:
            vouchers = session.scalars(select(Voucher).filter_by(**filters))
            return list(vouchers)

    def use_voucher(self, 
                    code: str) -> Voucher:

        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")

            voucher.used = True
            session.commit()

            return voucher

    def delete_voucher(self,
                       code: str) -> None:
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")
            session.delete(voucher)
            session.commit()


