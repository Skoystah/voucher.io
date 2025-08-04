from sqlalchemy import Boolean, CheckConstraint, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session, mapped_column, Mapped

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Voucher(Base):
    __tablename__ = "voucher"

    code: Mapped[str] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(2), CheckConstraint("duration in ('1h','2h','4h', '12h')", name="ck_duration"))
    used: Mapped[bool] = mapped_column(Boolean, CheckConstraint("used in (0,1)", name="ck_voucher_used"), default=False)
    

class DB():
    def __init__(self, db = "voucher.db", verbose=True):
        self.engine = create_engine(f'sqlite+pysqlite:///{db}', echo=verbose)

        Base.metadata.create_all(self.engine) 

    def add_voucher(self, voucher):
        with Session(self.engine) as session:
            try:
                session.add(voucher)
                # Expunging the object (removing from session) - otherwise its no longer available after flush
                # Maybe there is a more elegant solution (get object again from database? ...)
                session.commit()
                # session.expunge(voucher)
            except IntegrityError:
                session.rollback()
                raise KeyError("Voucher already exists")
            

    def get_voucher(self, code):
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")
            
            return voucher

    def get_vouchers(self, **kwargs):
        with Session(self.engine) as session:
            vouchers = session.scalars(select(Voucher).filter_by(**kwargs))
            return list(vouchers)

    def use_voucher(self, code):
        with Session(self.engine) as session:
            voucher = session.get(Voucher, code)
            if voucher is None:
                raise KeyError("Voucher does not exist")

            voucher.used = True
            session.commit()
            # session.expunge(voucher)
            return voucher




