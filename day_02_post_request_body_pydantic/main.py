from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    price: int


products = []


@app.post("/products")
def create_product(product: Product):
    product_data = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(product_data)
    return product_data


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product["id"] == product_id:
            product["name"] = updated_product.name
            product["price"] = updated_product.price

            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)

            return {
                "message": "Product is deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )