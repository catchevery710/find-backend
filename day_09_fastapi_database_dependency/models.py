from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

#数据库里的表长什么样？
#创建 ORM Model 的共同基础类。
Base = declarative_base()
#用 Python class 描述数据库表。 Python class 和数据库 table 的映射
#定义一个 SQLAlchemy ORM Model。
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