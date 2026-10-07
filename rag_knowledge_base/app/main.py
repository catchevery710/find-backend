from fastapi import FastAPI

from app.routers.documents import router as documents_router
from app.routers.ask import router as ask_router


app = FastAPI(
    title="RAG Knowledge Base API",
    version="1.0.0"
)

app.include_router(documents_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {
        "message": "RAG Knowledge Base API is running."
    }