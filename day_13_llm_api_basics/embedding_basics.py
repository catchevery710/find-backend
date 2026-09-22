import math
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI()


# texts = [
#     "I like dogs.",
#     "I love puppies.",
#     "MySQL stores data in tables."
# ]

# response = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=texts
# )

# embedding_a = response.data[0].embedding
# embedding_b = response.data[1].embedding
# embedding_c = response.data[2].embedding

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

    similarity = dot_product / (
    magnitude_a * magnitude_b
    )
    
    return similarity

# similarity_ab = cosine_similarity(
#     embedding_a,
#     embedding_b
# )

# similarity_ac = cosine_similarity(
#     embedding_a,
#     embedding_c
# )

# print("A vs B:", similarity_ab)
# print("A vs C:", similarity_ac)


documents = [
    "Dogs are popular household pets.",
    "MySQL is a relational database.",
    "Puppies need regular exercise and training.",
    "FastAPI is a Python framework for building APIs."
]

query = "How should I take care of a young dog?"


response = client.embeddings.create(
    model="text-embedding-3-small",
    input=documents + [query]
)


document_embeddings = [
    item.embedding
    for item in response.data[:-1]
]

query_embedding = response.data[-1].embedding

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

results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)

top_k = results[:2]

for result in top_k:
    print(
        result["similarity"],
        result["document"]
    )


context = "\n".join(
    result["document"]
    for result in top_k
)


#Grounded answer
# prompt = f"""
# Use the following context to answer the question.

# Context:
# {context}

# Question:
# {query}
# """



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


answer_response = client.responses.create(
    model="gpt-5.6-luna",
    input=prompt
)

print(answer_response.output_text)

