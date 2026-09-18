from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship

#数据库里的表长什么样？
#创建 ORM Model 的共同基础类。
Base = declarative_base()
#用 Python class 描述数据库表。 Python class 和数据库 table 的映射
#定义一个 SQLAlchemy ORM Model。
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    orders = relationship(
        "Order",
        back_populates="user"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    category = Column(
        String(100)
    )

    price = Column(
        Integer,
        nullable= False
    )

    orders = relationship(
        "Order",
        back_populates="product"
    )

class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    amount = Column(
        Integer,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    product = relationship(
        "Product",
        back_populates="orders"
    )