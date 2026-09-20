from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import User, Product, Order
from schemas import (
    OrderCreate,
    OrderResponse,
    OrderDetailResponse
)
from dependencies import (
    get_user_or_404,
    get_order_or_404
)

router = APIRouter()

@router.post(
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


@router.get(
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


@router.get(
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

@router.get("/users/{user_id}/order-products")
def get_user_order_products(
    user_id: int,
    db: Session = Depends(get_db)
):
    statement = (
        select(Order,Product)
        .join(
            Product,
            Order.product_id == Product.id
        )
        .where(
            Order.user_id == user_id
        )
    )

    results = db.execute(statement).all()

    return [
    {
        "order_id": order.id,
        "quantity": order.quantity,
        "amount": order.amount,
        "product_name": product.name,
        "product_price": product.price
    }
    for order, product in results
]