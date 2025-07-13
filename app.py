from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
import time

app = FastAPI()
engine = None

def init_engine():
    global engine
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    print(">> DEBUG: DB_URL =", DB_URL)

    retries = 5
    while retries > 0:
        try:
            engine = create_engine(DB_URL)
            with engine.connect():
                print("✅ DB 接続成功")
                break
        except OperationalError as e:
            print(f"❌ DB 接続失敗: {e}")
            retries -= 1
            time.sleep(5)

@app.on_event("startup")
def startup():
    init_engine()

@app.get("/")
def read_root():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello from PostgreSQL'")).fetchone()
        return {"message": result[0]}
