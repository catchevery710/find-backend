import math
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

client = OpenAI()

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


text = """
Retrieval-Augmented Generation combines information retrieval
with language model generation.

A RAG system first retrieves relevant information from a
knowledge base.

The retrieved information is then added to the prompt as context.

The language model uses that context to generate a grounded answer.
"""

words = text.split()

chunks = []
chunk_size = 10
chunk_overlap = 3

step = chunk_size - chunk_overlap

# for start in range(0, len(words), chunk_size):
#     end = start + chunk_size

#     chunk_words = words[start:end]

#     chunk = " ".join(chunk_words)

#     chunks.append(chunk)
for start in range(0,len(words),step):
    end = start + chunk_size

    chunk_words = words[start:end]

    chunk = " ".join(chunk_words)

    chunks.append(chunk)


# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i}:")
#     print(chunk)
#     print()


raw_paragraphs = text.strip().split("\n\n")

paragraphs = []

for paragraph in raw_paragraphs:
    cleaned_paragraph =" ".join(
        paragraph.split()
    )

    paragraphs.append(cleaned_paragraph)

# for i, paragraph in enumerate(paragraphs):
#     print(f"Paragraph {i}:")
#     print(paragraph)
#     print()

embedding_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=paragraphs
)

vector_store = []

for i in range(len(paragraphs)):
    vector_store.append(
        {
            "id":i,
            "text":paragraphs[i],
            "embedding":embedding_response.data[i].embedding
        }
    )

# for item in vector_store:
#     print("ID:", item["id"])
#     print("Text:", item["text"])
#     print("Vector length:", len(item["embedding"]))
#     print()

query = "How does RAG find useful information?"

query_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = query_response.data[0].embedding

results = []

for item in vector_store:
    similarity = cosine_similarity(
        query_embedding,
        item["embedding"]
    )

    results.append(
        {
            "id": item["id"],
            "text": item["text"],
            "similarity": similarity
        }
    )

results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)

top_k = results[:2]

print("\nRetrieved results:")

for item in top_k:
    print("ID:", item["id"])
    print("Similarity:", item["similarity"])
    print("Text:", item["text"])
    print()