from pydantic import BaseModel, ConfigDict,Field



# =========================
# User
# =========================

class UserCreate(BaseModel):
    name: str = Field(min_length=1,max_length=100)


class UserUpdate(BaseModel):
    name: str = Field(min_length=1,max_length=100)


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
    name: str = Field(min_length=1,max_length=100)

    # 可以不传
    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    price: int = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str | None
    price: int

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    price: int | None = Field(
        default=None,
        gt=0
    )

# =========================
# Order
# =========================

class OrderCreate(BaseModel):
    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

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