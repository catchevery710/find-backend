from fastapi import APIRouter,HTTPException,Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import User
from schemas import UserCreate,UserResponse,UserUpdate
from dependencies import get_user_or_404


router = APIRouter()

# =========================
# User CRUD
# =========================


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        name=user_data.name
    )

    db.add(new_user)

    # 把事务真正写入数据库
    db.commit()

    # 从数据库重新读取最新状态
    # 例如自动生成的 id
    db.refresh(new_user)

    return new_user


@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    statement = select(User)

    users = db.scalars(statement).all()

    return users


@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user: User = Depends(get_user_or_404)
):
    # 查询 + 404 已经交给 dependency
    return user


@router.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_data: UserUpdate,
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    user.name = user_data.name

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}")
def delete_user(
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    db.delete(user)

    try:
        db.commit()

    except IntegrityError:
        # commit 失败后 Session 进入失败状态
        # 必须 rollback 才能继续使用
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "User cannot be deleted because "
                "it is referenced by other data"
            )
        )

    return {
        "message": "User deleted"
    }
