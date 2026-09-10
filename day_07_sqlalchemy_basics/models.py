from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
#用 Python class 描述数据库表。 Python class 和数据库 table 的映射
class User(Base):
    __tablename__="users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

