from evaluation.evaluation_cases import evaluation_cases

from app.services.retrieval_service import retrieve_chunks
hit_at_1 = 0
hit_at_3 = 0

total_cases = len(evaluation_cases)


for case in evaluation_cases:
    question = case["question"]
    expected_source = case["expected_source"]
    expected_page = case["expected_page"]

    results = retrieve_chunks(
        question=question,
        top_k=3
    )

    retrieved_metadatas = results["metadatas"][0]

    print("Question:", question)
    print(
        "Expected:",
        expected_source,
        "page",
        expected_page
    )

    for i, metadata in enumerate(retrieved_metadatas):
        print(
            "Rank:",
            i + 1,
            "| Source:",
            metadata["source"],
            "| Page:",
            metadata["page"]
        )

    # Hit@1
    top_1 = retrieved_metadatas[0]

    if (
        top_1["source"] == expected_source
        and top_1["page"] == expected_page
    ):
        hit_at_1 += 1

    # Hit@3
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