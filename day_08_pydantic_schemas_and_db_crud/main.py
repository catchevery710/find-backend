from fastapi import FastAPI, HTTPException

from sqlalchemy import select

from database import SessionLocal
from models import User
from schemas import UserCreate, UserUpdate, UserResponse


# 创建 FastAPI Application
app = FastAPI()


# ==================================================
# CREATE
#
# POST /users
#
# Request JSON
#     ↓
# UserCreate
#     ↓
# SQLAlchemy User ORM Object
#     ↓
# Session
#     ↓
# MySQL
# ==================================================

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user(user_data: UserCreate):

    # 创建数据库 Session
    db = SessionLocal()

    # 从 Pydantic UserCreate 中拿数据
    #
    # 创建 SQLAlchemy ORM 对象
    new_user = User(
        name=user_data.name
    )

    # 把 ORM 对象交给 Session 管理
    db.add(new_user)

    # 真正提交事务
    # 数据写入 MySQL
    db.commit()

    # 从数据库重新读取最新状态
    # 例如数据库生成的 AUTO_INCREMENT id
    db.refresh(new_user)

    # 关闭 Session
    db.close()

    # SQLAlchemy ORM Object
    #        ↓
    # UserResponse
    #        ↓
    # JSON
    return new_user


# ==================================================
# READ ALL
#
# GET /users
# ==================================================

@app.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users():

    db = SessionLocal()

    # ORM：
    # SELECT * FROM users;
    statement = select(User)

    # 执行查询
    # .all() 获取所有 User ORM objects
    users = db.scalars(statement).all()

    db.close()

    return users


# ==================================================
# READ ONE
#
# GET /users/{user_id}
#
# 例如：
# GET /users/8
#
# user_id = 8
# ==================================================

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):

    db = SessionLocal()

    # 大致对应：
    #
    # SELECT *
    # FROM users
    # WHERE id = user_id;
    statement = select(User).where(
        User.id == user_id
    )

    # 只拿第一个结果
    user = db.scalars(statement).first()

    # 没找到
    if not user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.close()

    return user


# ==================================================
# UPDATE
#
# PUT /users/{user_id}
#
# 流程：
#
# 查
# ↓
# 修改 ORM 属性
# ↓
# commit
# ↓
# refresh
# ==================================================

@app.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_data: UserUpdate
):

    db = SessionLocal()

    statement = select(User).where(
        User.id == user_id
    )

    user = db.scalars(statement).first()

    if not user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 修改 Python ORM object
    user.name = user_data.name

    # SQLAlchemy 检测到对象发生变化
    # 然后把 UPDATE 提交到数据库
    db.commit()

    # 读取数据库最新状态
    db.refresh(user)

    db.close()

    return user


# ==================================================
# DELETE
#
# DELETE /users/{user_id}
#
# 流程：
#
# 查
# ↓
# delete
# ↓
# commit
# ==================================================

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    db = SessionLocal()

    statement = select(User).where(
        User.id == user_id
    )

    user = db.scalars(statement).first()

    if not user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 标记删除 ORM object
    db.delete(user)

    # 真正删除数据库记录
    db.commit()

    db.close()

    return {
        "message": "User deleted"
    }