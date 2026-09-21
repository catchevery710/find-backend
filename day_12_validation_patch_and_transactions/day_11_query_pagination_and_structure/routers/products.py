from fastapi import APIRouter, Depends,Query,HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Product
from dependencies import get_product_or_404
from schemas import ProductResponse, ProductUpdate
from typing import Literal

router = APIRouter()

@router.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    category: str | None = None,
    min_price: int | None = Query(
        default=None,
        gt=0
    ),

    max_price: int | None = Query(
        default=None,
        gt=0
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),

    sort_by: Literal["id", "price"] = "id",
    sort_order : Literal["asc","desc"] = "asc",

    db: Session = Depends(get_db)
):

    if (
    min_price is not None
    and max_price is not None
    and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price"
        )
    
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

@router.patch(
    "/products/{product_id}",
    response_model=ProductResponse
)

def update_product(
    product_data:ProductUpdate,
    product: Product = Depends(get_product_or_404),
    db: Session = Depends(get_db)
):
    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field,value in update_data.items():
        setattr(product,field,value)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Product update conflicts with database constraints"
        )

    db.refresh(product)

    return product

