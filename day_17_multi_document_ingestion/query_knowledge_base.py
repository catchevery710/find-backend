from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# =========================
# 1. 环境配置
# =========================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()


# =========================
# 2. 连接已有 Chroma Knowledge Base
# =========================

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

# 这里只负责查询已有 collection，
# 所以使用 get_collection()
collection = chroma_client.get_collection(
    name="multi_document_rag"
)


# =========================
# 3. 用户问题
# =========================

query = "Why is chunk overlap useful?"


# =========================
# 4. 给 Query 生成 Embedding
# =========================

query_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = query_response.data[0].embedding


# =========================
# 5. 跨所有 PDF 做 Top-K Retrieval
# =========================

results = collection.query(
    # Chroma 支持一次查询多个向量，
    # 所以即使只有一个 query，也需要套一层 list
    query_embeddings=[query_embedding],

    # 返回最相关的 3 个 chunk
    n_results=3
)


# =========================
# 6. 查看检索结果
# =========================

# results 是嵌套结构：
# [0] 表示第一个 query 的结果
for i in range(len(results["documents"][0])):

    document = results["documents"][0][i]
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]

    print("Rank:", i + 1)

    # metadata 让我们可以追溯来源
    print("Source:", metadata["source"])
    print("Page:", metadata["page"])

    # cosine distance：
    # 越小通常表示越相似
    print("Distance:", distance)

    print("Text:", document)
    print()