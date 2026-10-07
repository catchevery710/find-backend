from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR.parent
PROJECT_DIR = APP_DIR.parent
BACKEND_DIR = PROJECT_DIR.parent

load_dotenv(BACKEND_DIR / ".env")


openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path=str(PROJECT_DIR / "chroma_data")
)

collection = chroma_client.get_collection(
    name="rag_knowledge_base"
)





def retrieve_chunks(question: str, top_k: int = 3):
    # 1. 把用户问题转成 embedding
    query_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = query_response.data[0].embedding

    # 2. 在向量数据库中寻找最相关的 Top-K chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results