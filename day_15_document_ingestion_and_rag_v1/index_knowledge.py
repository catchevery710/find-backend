from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. Paths and environment
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()


# ============================================================
# 2. Load document
# ============================================================

file_path = BASE_DIR / "knowledge.txt"

text = file_path.read_text(
    encoding="utf-8"
)


# ============================================================
# 3. Paragraph-based chunking
# ============================================================

raw_paragraphs = text.strip().split("\n\n")

paragraphs = []

for paragraph in raw_paragraphs:
    cleaned_paragraph = " ".join(
        paragraph.split()
    )

    paragraphs.append(cleaned_paragraph)


# ============================================================
# 4. Generate document embeddings
# ============================================================

embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=paragraphs
)

paragraph_embeddings = [
    item.embedding
    for item in embedding_response.data
]


# ============================================================
# 5. Generate chunk IDs automatically
# ============================================================

ids = [
    f"chunk_{i}"
    for i in range(len(paragraphs))
]


# ============================================================
# 6. Connect to persistent Chroma
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_or_create_collection(
    name="rag_v1",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)


# ============================================================
# 7. Store chunks in vector store
# ============================================================

collection.upsert(
    ids=ids,
    documents=paragraphs,
    embeddings=paragraph_embeddings
)


print("Indexed chunks:", collection.count())