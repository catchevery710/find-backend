from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from schemas import ProductResponse


router = APIRouter()

@router.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "id",
    sort_order : str = "asc",
    db: Session = Depends(get_db)
):
    statement = select(Product)

    if category is not None:
        statement = statement.where(
            Product.category==category
        )

    if min_price is not None:
        statement = statement.where(
            Product.price >= min_price
        )

    if max_price is not None:
        statement = statement.where(
            Product.price <= max_price
        )

    if sort_by == "price":
        sort_column = Product.price
    else:
        sort_column  = Product.id

    if sort_order == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    statement = statement.limit(limit).offset(offset)

    products = db.scalars(statement).all()

    return products