from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

documents = [
    "Retrieval-Augmented Generation combines information retrieval with language model generation.",
    "A RAG system first retrieves relevant information from a knowledge base.",
    "The retrieved information is then added to the prompt as context.",
    "The language model uses that context to generate a grounded answer."
]

embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=documents
)

document_embeddings = [
    item.embedding
    for item in embedding_response.data
]

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_or_create_collection(
    name="rag_basics",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

ids = [
    "chunk_0",
    "chunk_1",
    "chunk_2",
    "chunk_3"
]

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=document_embeddings
)

query = "How does RAG find useful information?"

query_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = query_response.data[0].embedding


#Chroma 的 query() 会直接给你最相关的结果
# distance 越小
# → 越相似
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(results["documents"][0])
print(results["distances"][0])