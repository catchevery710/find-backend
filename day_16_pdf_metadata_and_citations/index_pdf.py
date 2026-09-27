from pathlib import Path
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

pdf_path = BASE_DIR / "knowledge.pdf"

reader = PdfReader(pdf_path)

pages = []

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()

    cleaned_text = " ".join(text.split())

    pages.append(
        {
            "source": pdf_path.name,
            "page": page_number,
            "text": cleaned_text
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

    for start in range(0, len(words), step):
        end = start + chunk_size

        chunk_words = words[start:end]

        if len(chunk_words) <= chunk_overlap and start != 0:
            continue

        chunk_text = " ".join(chunk_words)

        chunks.append(
            {
                "text": chunk_text,
                "source": source,
                "page": page_number
            }
        )

chunk_texts = [
    chunk["text"]
    for chunk in chunks
]

metadatas = [
    {
        "source": chunk["source"],
        "page": chunk["page"]
    }
    for chunk in chunks
]

ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]

embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=chunk_texts
)

chunk_embeddings = [
    item.embedding
    for item in embedding_response.data
]

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_or_create_collection(
    name="pdf_rag",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

collection.upsert(
    ids=ids,
    documents=chunk_texts,
    embeddings=chunk_embeddings,
    metadatas=metadatas
)

print("Stored chunks:", collection.count())