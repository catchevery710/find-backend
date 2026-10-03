from fastapi import FastAPI,UploadFile,File
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

app = FastAPI()


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    content = await file.read()

    pdf_stream = BytesIO(content)

    reader = PdfReader(pdf_stream)

    pages = []

    for page_number,page in enumerate(reader.pages,start = 1):
        text = page.extract_text()

        cleaned_text = " ".join(text.split())

        pages.append(
            {
                "source":file.filename,
                "page":page_number,
                "text":cleaned_text
            }
        )

    chunks = []

    for page_item in pages:
        page_text = page_item["text"]
        source = page_item["source"]
        page_number = page_item["page"]

        words = page_text.split()

        chunk_size = 60
        chunk_overlap = 15
        step = chunk_size - chunk_overlap

        chunk_index = 0

        for start in range(0,len(words),step):
            end = start + chunk_size

            chunk_words = words[start:end]

            if len(chunk_words) <= chunk_overlap and start !=0:
                continue

            chunk_text = " ".join(chunk_words)

            chunk_id = (
                f"{Path(source).stem}_"
                f"p{page_number}_"            
                f"c{chunk_index}"
            )

            chunks.append(
            {
                "id": chunk_id,
                "text": chunk_text,
                "source": source,
                "page": page_number
            }
        )

            chunk_index += 1

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
    chunk["id"]
    for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=documents
    )

    embeddings = [
        item.embedding
        for item in embedding_response.data
    ]

    chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
    )

    collection = chroma_client.get_or_create_collection(
        name="rag_upload_api",
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
    )

    return {
    "filename": file.filename,
    "chunk_count": len(chunks),
    "stored_chunks": collection.count()
}