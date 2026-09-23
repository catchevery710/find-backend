from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. Load environment variables
# ============================================================
# 当前文件所在目录：
# backend/day_14_chunking_and_vector_store/
BASE_DIR = Path(__file__).resolve().parent

# 项目根目录：
# backend/
PROJECT_ROOT = BASE_DIR.parent

# 从 backend/.env 加载 OPENAI_API_KEY
load_dotenv(PROJECT_ROOT / ".env")

# OpenAI API client
openai_client = OpenAI()


# ============================================================
# 2. Connect to the existing persistent Chroma database
# ============================================================
# chroma_data 中已经保存了文档的：
# - ids
# - documents
# - embeddings
#
# 所以查询时不需要重新计算 document embeddings。
chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)


# ============================================================
# 3. Open the existing collection
# ============================================================
# rag_basics 已经由 index_documents.py 创建并写入数据。
#
# get_collection():
# 打开已经存在的 collection。
#
# 这里不是 get_or_create_collection()，
# 因为 Retrieval 阶段默认知识库已经建立完成。
collection = chroma_client.get_collection(
    name="rag_basics"
)


# ============================================================
# 4. User query
# ============================================================
query = "How does RAG find useful information?"


# ============================================================
# 5. Convert only the query into an embedding
# ============================================================
# 文档 embedding 已经在 Indexing 阶段算过并存进 Chroma。
#
# 每次用户提出新的问题时，
# 只需要重新计算 query embedding。
query_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

# 当前只有一个 query，
# 所以拿 response.data[0]。
query_embedding = query_response.data[0].embedding


# ============================================================
# 6. Search the vector store
# ============================================================
# query_embeddings=[query_embedding]
# → 用当前 query 的向量进行搜索。
#
# 外面需要 []，因为 Chroma 支持一次查询多个 query embeddings。
#
# n_results=2
# → 返回最相关的两个结果，也就是 Top-2 Retrieval。
#
# Chroma 会替我们完成：
# 1. 向量相似度 / 距离计算
# 2. 排序
# 3. Top-K 选择
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


# ============================================================
# 7. Display retrieved documents
# ============================================================
# results["documents"] 是二维结构：
#
# [
#     [query_0 的 Top-K 结果],
#     [query_1 的 Top-K 结果],
#     ...
# ]
#
# 因为当前只有一个 query：
#
# results["documents"][0]
# → 第 0 个 query 的所有 Top-K documents
#
# results["documents"][0][i]
# → 第 0 个 query 的第 i 个 retrieval result
#
# distances 的位置与 documents 一一对应。
#
# 对 cosine distance 来说：
# distance 越小 → 两个向量越接近。
for i in range(len(results["documents"][0])):
    print("Document:", results["documents"][0][i])
    print("Distance:", results["distances"][0][i])
    print()