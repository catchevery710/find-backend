from fastapi import FastAPI, HTTPException

app = FastAPI()


# -------------------------
# Mock Data
# 模拟数据库
# -------------------------

users = {
    1: {
        "name": "Tom",
        "age": 20
    },
    2: {
        "name": "Jack",
        "age": 25
    }
}


products = {
    1: {
        "name": "Phone",
        "price": 1000
    },
    2: {
        "name": "Laptop",
        "price": 2000
    }
}


# -------------------------
# Basic GET
# -------------------------

@app.get("/")
def root():
    return {
        "message": "Hello World"
    }


# -------------------------
# Path Parameter
# GET /users/1
# -------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]


# -------------------------
# Path Parameter
# GET /products/1
# -------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return products[product_id]


# -------------------------
# Two Path Parameters
# GET /users/1/orders/7
# -------------------------

@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {
        "user_id": user_id,
        "order_id": order_id
    }


# -------------------------
# Query Parameter
# GET /search?q=python
# -------------------------

@app.get("/search")
def search(q: str):
    return {
        "query": q
    }


# -------------------------
# Query Parameters + Default Value
# GET /items?category=phone
# GET /items?category=phone&page=2
# -------------------------

@app.get("/items")
def get_items(category: str, page: int = 1):
    return {
        "category": category,
        "page": page
    }