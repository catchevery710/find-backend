import chromadb

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from evaluation_cases import evaluation_cases


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DAY18_DIR = PROJECT_ROOT / "day_18_rag_upload_api"

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path=str(DAY18_DIR / "chroma_data")
)

collection = chroma_client.get_collection(
    name="rag_upload_api"
)

def retrieve(question, top_k=3):
    query_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = query_response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


hit_at_1 = 0
hit_at_3 = 0
total_cases = len(evaluation_cases)


for case in evaluation_cases:
    question = case["question"]
    expected_source = case["expected_source"]
    expected_page = case["expected_page"]

    results = retrieve(question, top_k=3)

    print("Question:", question)
    print("Expected:", expected_source, "page", expected_page)

    retrieved_metadatas = results["metadatas"][0]

    for i, metadata in enumerate(retrieved_metadatas):
        print(
            "Rank:",
            i + 1,
            "| Source:",
            metadata["source"],
            "| Page:",
            metadata["page"]
        )

    # Hit@1：
    # 第一名是否命中 expected source + page
    top_1 = retrieved_metadatas[0]

    if (
        top_1["source"] == expected_source
        and top_1["page"] == expected_page
    ):
        hit_at_1 += 1

    # Hit@3：
    # 前三名中是否至少有一条命中 expected source + page
    for metadata in retrieved_metadatas:
        if (
            metadata["source"] == expected_source
            and metadata["page"] == expected_page
        ):
            hit_at_3 += 1
            break

    print()



hit_at_1_score = hit_at_1 / total_cases
hit_at_3_score = hit_at_3 / total_cases

print("Hit@1:", hit_at_1_score)
print("Hit@3:", hit_at_3_score)