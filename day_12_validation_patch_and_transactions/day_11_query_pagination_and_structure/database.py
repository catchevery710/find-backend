import os
from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


# 当前 database.py 所在目录
BASE_DIR = Path(__file__).resolve().parent


# 加载 .env 中的数据库配置
load_dotenv(
    BASE_DIR / ".env",
    override=True
)


# 构建数据库连接地址
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME")
)


# Engine：SQLAlchemy 连接数据库的入口
engine = create_engine(
    DATABASE_URL,
    echo=True
)


# SessionLocal：创建数据库 Session 的工厂
SessionLocal = sessionmaker(
    bind=engine
)


# FastAPI 数据库依赖
# 每个 request 创建一个 Session
# request 结束后自动关闭
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()