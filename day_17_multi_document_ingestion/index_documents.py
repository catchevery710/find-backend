from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader


# =========================
# 1. 基础路径与环境变量
# =========================

# 当前 day_17_multi_document_ingestion 文件夹
BASE_DIR = Path(__file__).resolve().parent

# backend 项目根目录
PROJECT_ROOT = BASE_DIR.parent

# 存放多个 PDF 的子文件夹
DOCUMENTS_DIR = BASE_DIR / "documents"

# 加载项目根目录中的 .env
load_dotenv(PROJECT_ROOT / ".env")

# OpenAI 客户端
openai_client = OpenAI()


# =========================
# 2. 自动扫描所有 PDF
# =========================

# 找到 documents/ 文件夹下所有 .pdf 文件
pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

print("PDF files found:", len(pdf_files))

for pdf_file in pdf_files:
    print("-", pdf_file.name)


# =========================
# 3. 逐个 PDF、逐页读取文本
# =========================

pages = []

for pdf_file in pdf_files:
    # 打开当前 PDF
    reader = PdfReader(pdf_file)

    # start=1，让页码从 1 开始，方便以后 citation
    for page_number, page in enumerate(reader.pages, start=1):

        # 提取这一页的文本
        text = page.extract_text()

        # 把多余换行、空格统一成普通空格
        cleaned_text = " ".join(text.split())

        # 保存正文 + 来源信息
        pages.append(
            {
                "source": pdf_file.name,
                "page": page_number,
                "text": cleaned_text
            }
        )

print("Pages loaded:", len(pages))


# =========================
# 4. 每一页继续做 Chunking
# =========================

chunks = []

for page_item in pages:

    # 当前页的正文
    page_text = page_item["text"]

    # 当前页来自哪份 PDF
    source = page_item["source"]

    # 当前页页码
    page_number = page_item["page"]

    # 按空格切成单词列表
    words = page_text.split()

    # 每个 chunk 最多 60 个词
    chunk_size = 60

    # 相邻 chunk 重复 15 个词
    # 用来减少切块边界造成的上下文丢失
    chunk_overlap = 15

    # 每次实际向前移动 45 个词
    step = chunk_size - chunk_overlap

    # 当前页内部的 chunk 编号
    chunk_index = 0

    for start in range(0, len(words), step):

        end = start + chunk_size

        chunk_words = words[start:end]

        # 如果最后剩余的内容小于等于 overlap，
        # 通常已经完整包含在上一个 chunk 中，
        # 就不再创建一个几乎重复的小 chunk
        if len(chunk_words) <= chunk_overlap and start != 0:
            continue

        # 单词列表重新组成字符串
        chunk_text = " ".join(chunk_words)

        # 去掉文件扩展名
        # chunking.pdf -> chunking
        source_stem = Path(source).stem

        # 给每个 chunk 一个可读、稳定的 ID
        # 例如：
        # chunking_p2_c1
        chunk_id = f"{source_stem}_p{page_number}_c{chunk_index}"

        chunks.append(
            {
                "id": chunk_id,
                "text": chunk_text,
                "source": source,
                "page": page_number
            }
        )

        chunk_index += 1

print("Chunks created:", len(chunks))


# =========================
# 5. 准备 Chroma 所需的数据
# =========================

# 每个 chunk 的唯一 ID
ids = [
    chunk["id"]
    for chunk in chunks
]

# 真正用于 embedding / retrieval 的文本
documents = [
    chunk["text"]
    for chunk in chunks
]

# metadata 保存来源信息
# retrieval 后可以知道文本来自哪份 PDF、哪一页
metadatas = [
    {
        "source": chunk["source"],
        "page": chunk["page"]
    }
    for chunk in chunks
]


# =========================
# 6. 为所有 Chunk 生成 Embedding
# =========================

embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=documents
)

embeddings = [
    item.embedding
    for item in embedding_response.data
]

# 四组数据必须一一对应
print("ids:", len(ids))
print("documents:", len(documents))
print("metadatas:", len(metadatas))
print("embeddings:", len(embeddings))


# =========================
# 7. 写入持久化 Chroma
# =========================

chroma_client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_data")
)

collection = chroma_client.get_or_create_collection(
    name="multi_document_rag",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

# upsert：
# ID 已存在 -> 更新
# ID 不存在 -> 插入
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Stored chunks:", collection.count())