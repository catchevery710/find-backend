from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_collection(
    name="pdf_rag"
)

query = "How do citations improve a RAG system?"

query_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = query_response.data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context_parts = []

for i in range(len(results["documents"][0])):
    document = results["documents"][0][i]
    metadata = results["metadatas"][0][i]

    source = metadata["source"]
    page = metadata["page"]

    context_part = (
        f"[Source: {source}, Page: {page}]\n"
        f"{document}"
    )

    context_parts.append(context_part)

context = "\n\n".join(context_parts)


prompt = f"""
Answer the question using only the information provided in the context.

Include citations in the answer using this format:
[Source: filename, Page: number]

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

print("Question:")
print(query)

print("\nAnswer:")
print(answer_response.output_text)