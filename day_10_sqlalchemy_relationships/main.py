from fastapi import (
    FastAPI,
    HTTPException,
    Depends
)

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from database import get_db

from models import (
    User,
    Product,
    Order
)

from schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    OrderCreate,
    OrderResponse,
    OrderDetailResponse
)


app = FastAPI()


# =========================
# Shared Dependencies
# =========================


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


# =========================
# User CRUD
# =========================


@app.post(
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


@app.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    statement = select(User)

    users = db.scalars(statement).all()

    return users


@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user: User = Depends(get_user_or_404)
):
    # 查询 + 404 已经交给 dependency
    return user


@app.put(
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


@app.delete("/users/{user_id}")
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


# =========================
# Order
# =========================


@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    # ---------- 检查 User ----------

    user_statement = select(User).where(
        User.id == order_data.user_id
    )

    user = db.scalars(
        user_statement
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    # ---------- 检查 Product ----------

    product_statement = select(Product).where(
        Product.id == order_data.product_id
    )

    product = db.scalars(
        product_statement
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    # ---------- Business Logic ----------

    # amount 由服务端计算
    # 客户端不能自己决定订单金额
    amount = (
        product.price
        * order_data.quantity
    )


    # ---------- 创建 Order ----------

    new_order = Order(
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        amount=amount
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@app.get(
    "/users/{user_id}/orders",
    response_model=list[OrderResponse]
)
def get_user_orders(
    user: User = Depends(get_user_or_404)
):
    # relationship：
    #
    # User.orders
    # → 对应这个用户的 Order 对象列表
    return user.orders


@app.get(
    "/orders/{order_id}",
    response_model=OrderDetailResponse
)
def get_order(
    order: Order = Depends(get_order_or_404)
):
    # OrderDetailResponse 会读取：
    #
    # order.id
    # order.quantity
    # order.amount
    # order.user
    # order.product
    #
    # 其中 user / product 来自 relationship
    return order