from fastapi import APIRouter

from app.schemas.rag import AskRequest
from app.services.rag_service import answer_question


router = APIRouter(
    tags=["rag"]
)


@router.post("/ask")
async def ask_question(request: AskRequest):
    result = answer_question(
        question=request.question
    )

    return result