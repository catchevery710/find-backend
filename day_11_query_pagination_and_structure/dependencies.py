from fastapi import HTTPException,Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import User,Order

def get_user_or_404(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    公共依赖：

    根据 user_id 查询 User。

    找不到：
        直接返回 404。

    找到：
        返回 User ORM 对象。
    """

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


def get_order_or_404(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    根据 order_id 查询 Order。

    不存在：
        404

    存在：
        返回 Order ORM 对象
    """

    statement = select(Order).where(
        Order.id == order_id
    )

    order = db.scalars(statement).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order
