from fastapi import FastAPI

from routers.users import router as users_router
from routers.products import router as products_router
from routers.orders import router as orders_router


app = FastAPI()


app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
