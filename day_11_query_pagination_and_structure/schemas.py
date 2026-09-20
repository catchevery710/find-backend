from pydantic import BaseModel, ConfigDict


# =========================
# User
# =========================

class UserCreate(BaseModel):
    name: str


class UserUpdate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str

    # 允许从 SQLAlchemy ORM 对象读取属性
    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# Product
# =========================

class ProductCreate(BaseModel):
    name: str

    # 可以不传
    category: str | None = None

    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str | None
    price: int

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# Order
# =========================

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    # 注意：
    # 客户端不能传 amount
    # amount 由后端根据商品价格计算


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    amount: int

    model_config = ConfigDict(
        from_attributes=True
    )


# Order 详情接口
# 不只返回 user_id / product_id
# 而是返回完整 User / Product
class OrderDetailResponse(BaseModel):
    id: int
    quantity: int
    amount: int

    user: UserResponse
    product: ProductResponse

    model_config = ConfigDict(
        from_attributes=True
    )