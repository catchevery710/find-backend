import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. Load environment variables
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI()


# ============================================================
# 2. Cosine Similarity
# Compare two embedding vectors
# ============================================================

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        x * y
        for x, y in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(y * y for y in vector_b)
    )

    return dot_product / (
        magnitude_a * magnitude_b
    )


# ============================================================
# 3. Documents and user query
# ============================================================

documents = [
    "Dogs are popular household pets.",
    "MySQL is a relational database.",
    "Puppies need regular exercise and training.",
    "FastAPI is a Python framework for building APIs."
]

query = "How should I take care of a young dog?"


# ============================================================
# 4. Convert text into embeddings
# ============================================================

embedding_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=documents + [query]
)

# First embeddings belong to documents
document_embeddings = [
    item.embedding
    for item in embedding_response.data[:-1]
]

# Last embedding belongs to the query
query_embedding = embedding_response.data[-1].embedding


# ============================================================
# 5. Semantic retrieval
# Compare query vector with every document vector
# ============================================================

results = []

for document, document_embedding in zip(
    documents,
    document_embeddings
):
    similarity = cosine_similarity(
        query_embedding,
        document_embedding
    )

    results.append(
        {
            "document": document,
            "similarity": similarity
        }
    )


# ============================================================
# 6. Sort and retrieve Top-K
# ============================================================

results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)

top_k = results[:2]

print("Retrieved documents:")

for result in top_k:
    print(
        result["similarity"],
        result["document"]
    )


# ============================================================
# 7. Build context
# ============================================================

context = "\n".join(
    result["document"]
    for result in top_k
)


# ============================================================
# 8. Augment the prompt with retrieved context
# ============================================================

prompt = f"""
Answer the question using only the information provided in the context.

If the context does not contain enough information to fully answer the question,
say that the available context is insufficient.

Do not add information from your own knowledge.

Context:
{context}

Question:
{query}
"""


# ============================================================
# 9. Generate grounded answer
# ============================================================

answer_response = client.responses.create(
    model="gpt-5.6-luna",
    input=prompt
)

print("\nAnswer:")
print(answer_response.output_text)