import chromadb

from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. 项目路径
# ============================================================

# 当前文件所在目录：
# backend/day_19_rag_query_api/
BASE_DIR = Path(__file__).resolve().parent

# backend 项目根目录
PROJECT_ROOT = BASE_DIR.parent

# Day18 中保存了已经建立好的 Chroma 向量数据库
DAY18_DIR = PROJECT_ROOT / "day_18_rag_upload_api"


# ============================================================
# 2. 加载环境变量 + OpenAI Client
# ============================================================

# 从 backend/.env 读取 OPENAI_API_KEY
load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()


# ============================================================
# 3. 连接 Day18 已经建立好的 Chroma Knowledge Base
# ============================================================

# Day18 的 /documents/upload 已经负责：
#
# PDF
# → parse
# → chunk
# → embedding
# → Chroma
#
# 所以 Day19 不需要重新处理 PDF，
# 只需要连接已有数据库进行 retrieval。

chroma_client = chromadb.PersistentClient(
    path=str(DAY18_DIR / "chroma_data")
)

# 查询已经存在的 collection
collection = chroma_client.get_collection(
    name="rag_upload_api"
)


# ============================================================
# 4. 定义 /ask 请求体
# ============================================================

class AskRequest(BaseModel):
    # 用户必须提交一个字符串类型的问题
    question: str


# ============================================================
# 5. 创建 FastAPI 应用
# ============================================================

app = FastAPI()


# ============================================================
# 6. RAG Query API
# ============================================================

@app.post("/ask")
async def ask_question(request: AskRequest):

    # --------------------------------------------------------
    # Step 1: 获取用户问题
    # --------------------------------------------------------

    query = request.question


    # --------------------------------------------------------
    # Step 2: 把 Query 转成 Embedding
    # --------------------------------------------------------

    # Document chunks 在 Day18 已经生成过 embeddings。
    #
    # 查询时只需要计算当前 query 的 embedding，
    # 不应该重新计算所有 document embeddings。

    query_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    # 当前只有一个 query，
    # 所以取第 0 个 embedding
    query_embedding = query_response.data[0].embedding


    # --------------------------------------------------------
    # Step 3: Top-K Semantic Retrieval
    # --------------------------------------------------------

    results = collection.query(
        # Chroma 支持一次查询多个向量，
        # 因此单个 query embedding 也需要放进 list
        query_embeddings=[query_embedding],

        # 找最相关的 3 个 chunks
        n_results=3
    )


    # --------------------------------------------------------
    # Step 4: 提取结构化 Sources
    # --------------------------------------------------------

    # sources 最终会直接作为 JSON 返回给前端。
    #
    # 这样 citation 不完全依赖 LLM 自己生成，
    # 程序也保存了真正 retrieval 得到的来源。

    sources = []

    for metadata in results["metadatas"][0]:

        source_item = {
            "source": metadata["source"],
            "page": metadata["page"]
        }

        # Top-K 可能有多个 chunk 来自同一页。
        #
        # 例如：
        # chunking.pdf Page 2
        # chunking.pdf Page 2
        # chunking.pdf Page 2
        #
        # 所以这里做简单去重。
        if source_item not in sources:
            sources.append(source_item)


    # --------------------------------------------------------
    # Step 5: 构造带 Citation Information 的 Context
    # --------------------------------------------------------

    context_parts = []

    # Chroma results 是嵌套结构：
    #
    # results["documents"][0]
    #
    # 第一个 [0]：
    # 表示第一个 query 的 retrieval results。

    for i in range(len(results["documents"][0])):

        # 第 i 个 retrieved chunk
        document = results["documents"][0][i]

        # 与该 chunk 对应的 metadata
        metadata = results["metadatas"][0][i]

        source = metadata["source"]
        page = metadata["page"]

        # 给每个 chunk 加上来源信息。
        #
        # LLM 看到的不再只是：
        #
        #   Chunk overlap...
        #
        # 而是：
        #
        #   [Source: chunking.pdf, Page: 2]
        #   Chunk overlap...
        #
        # 这样 LLM 才知道证据来自哪里。
        context_part = (
            f"[Source: {source}, Page: {page}]\n"
            f"{document}"
        )

        context_parts.append(context_part)


    # 把多个 Top-K chunks 拼成一个完整 context
    context = "\n\n".join(context_parts)


    # --------------------------------------------------------
    # Step 6: 构造 Grounded RAG Prompt
    # --------------------------------------------------------

    prompt = f"""
Answer the question using only the information provided in the context.

Include citations using this format:
[Source: filename, Page: number]

If the context does not contain enough information,
say that the available context is insufficient.

Context:
{context}

Question:
{query}
"""


    # --------------------------------------------------------
    # Step 7: 调用 LLM 生成最终答案
    # --------------------------------------------------------

    answer_response = openai_client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    answer = answer_response.output_text


    # --------------------------------------------------------
    # Step 8: 返回结构化 API Response
    # --------------------------------------------------------

    return {
        # 用户原始问题
        "question": query,

        # LLM 基于 retrieved context 生成的回答
        "answer": answer,

        # 程序根据 retrieval metadata 生成的来源
        "sources": sources
    }