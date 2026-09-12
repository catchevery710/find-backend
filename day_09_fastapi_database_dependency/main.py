from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI()


# ==================================================
# SHARED DEPENDENCY
#
# 根据 user_id 查询用户
#
# 找到：
# → 返回 User ORM object
#
# 找不到：
# → 直接返回 404
# ==================================================

def get_user_or_404(
    user_id: int,
    db: Session = Depends(get_db)
):

    statement = select(User).where(
        User.id == user_id
    )

    user = db.scalars(statement).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


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
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    # 根据 Pydantic 请求数据
    # 创建 SQLAlchemy ORM object
    new_user = User(
        name=user_data.name
    )

    # 把新对象加入 Session
    db.add(new_user)

    # 提交事务
    db.commit()

    # 从数据库读取最新状态
    # 例如 AUTO_INCREMENT 生成的 id
    db.refresh(new_user)

    return new_user


# ==================================================
# READ ALL
#
# GET /users
#
# 查询全部用户
# ==================================================

@app.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    statement = select(User)

    # .all()
    # 获取所有 User ORM objects
    users = db.scalars(statement).all()

    return users


# ==================================================
# READ ONE
#
# GET /users/{user_id}
#
# 用户查询和 404
# 已经交给 get_user_or_404()
# ==================================================

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user: User = Depends(get_user_or_404)
):

    return user


# ==================================================
# UPDATE
#
# PUT /users/{user_id}
#
# get_user_or_404()
# → 负责查用户
#
# update_user()
# → 只负责修改数据
# ==================================================

@app.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_data: UserUpdate,
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):

    # 修改 ORM object
    user.name = user_data.name

    # 提交 UPDATE
    db.commit()

    # 重新获取数据库最新状态
    db.refresh(user)

    return user


# ==================================================
# DELETE
#
# DELETE /users/{user_id}
#
# get_user_or_404()
# → 负责查用户
#
# delete_user()
# → 负责删除 + transaction error handling
# ==================================================

@app.delete("/users/{user_id}")
def delete_user(
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):

    # 标记删除 ORM object
    db.delete(user)

    try:
        # 真正提交 DELETE
        db.commit()

    except IntegrityError:

        # commit 失败后恢复 Session
        db.rollback()

        # 例如：
        # orders.user_id
        # 仍然引用当前 users.id
        raise HTTPException(
            status_code=409,
            detail=(
                "User cannot be deleted "
                "because it is referenced by other data"
            )
        )

    return {
        "message": "User deleted"
    }

