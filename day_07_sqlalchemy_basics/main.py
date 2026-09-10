from sqlalchemy import select

from database import SessionLocal
from models import User

#→ 真正操作数据库的工作区
db = SessionLocal()


#用 Python 对象完成增删改查
#1. select
statement = select(User).where(User.id == 1)

user = db.scalars(statement).first()

if user:
    print(user.id,user.name)


#2. insert
new_user = User(
    id=4,
    name = "David"
)

db.add(new_user)

db.commit()


#3. update
statement = select(User).where(User.id == 4)

user = db.scalars(statement).first()

if user:
    user.name = "Daniel"

db.commit()


#4. delete
statement = select(User).where(User.id==4)

user =db.scalars(statement).first()

if user:
    db.delete(user)
    db.commit()

db.close()