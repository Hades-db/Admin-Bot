from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class WarnRecord(Base):
    __tablename__ = 'warn_records'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    warns_count: Mapped[int] = mapped_column(Integer, default=0)