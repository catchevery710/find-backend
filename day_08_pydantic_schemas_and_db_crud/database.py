import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


#找到 database.py 当前所在文件夹。
BASE_DIR = Path(__file__).resolve().parent
#加载这个文件夹里的 .env。
load_dotenv(BASE_DIR/".env",override=True)


#根据 .env 组装数据库地址。
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME"),
)

engin = create_engine(
    DATABASE_URL,
    #SQLAlchemy 执行 SQL 时，把 SQL 打印到 Terminal。
    echo = True 
)

SessionLocal = sessionmaker(
    bind = engin
)

