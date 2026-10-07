from openai import OpenAI

from app.services.retrieval_service import retrieve_chunks


openai_client = OpenAI()


def answer_question(question: str):
    # 1. Retrieval
    results = retrieve_chunks(
        question=question,
        top_k=3
    )


    # 2. 构造结构化 sources
    sources = []

    for metadata in results["metadatas"][0]:
        source_item = {
            "source": metadata["source"],
            "page": metadata["page"]
        }

        # 去掉重复 source/page
        if source_item not in sources:
            sources.append(source_item)


    # 3. 构造给 LLM 使用的 context
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


    # 4. Grounded Prompt
    prompt = f"""
Answer the question using only the information provided in the context.

Include citations using this format:
[Source: filename, Page: number]

If the context does not contain enough information,
say that the available context is insufficient.

Context:
{context}

Question:
{question}
"""


    # 5. LLM Generation
    answer_response = openai_client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    answer = answer_response.output_text


    # 6. 返回业务结果
    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }