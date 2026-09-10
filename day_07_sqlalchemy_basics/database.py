import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR/".env",override = True)

#把零散的数据库配置组成一个完整数据库地址。
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host =os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT","3306")),
    database=os.getenv("DB_NAME"),
)

#SQLAlchemy 访问数据库的核心入口
engine = create_engine(
    DATABASE_URL,
    echo = True
)

#创建 Session 的工厂
SessionLocal = sessionmaker(
    bind = engine
)