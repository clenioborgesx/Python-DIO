import sqlalchemy as sqlA
import pymongo

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()

class User(Base):
    __table_name__= "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    adress = relationship(
        "Adress", back_populates="user", cascade="all, delete-ophan"
    )

class Address(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_adress = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="user")

    def __repr__(self):
        return f"Adress ()"