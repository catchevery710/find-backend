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
# 2. Connect to existing Chroma database
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_collection(
    name="rag_v1"
)

# ============================================================
# 3. User query
# ============================================================

query = "Why does RAG use a vector store?"

# ============================================================
# 4. Generate query embedding
# ============================================================

query_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = query_response.data[0].embedding

# ============================================================
# 5. Retrieve Top-K chunks
# ============================================================

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

# for i in range(len(results["documents"][0])):
#     print("Document:", results["documents"][0][i])
#     print("Distance:", results["distances"][0][i])
#     print()

context = "\n".join(
    results["documents"][0]
)

print(context)

prompt = f"""
Answer the question using only the information provided in the context.

If the context does not contain enough information,
say that the available context is insufficient.

Context:
{context}

Question:
{query}
"""

answer_response = openai_client.responses.create(
    model="gpt-5.6-luna",
    input=prompt
)

print(answer_response.output_text)