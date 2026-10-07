from fastapi import APIRouter, UploadFile, File

from app.services.ingestion_service import index_pdf


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    file_bytes = await file.read()

    result = index_pdf(
        file_bytes=file_bytes,
        filename=file.filename
    )

    return result