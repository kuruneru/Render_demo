from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, echo=True)

@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        # データ挿入（初回のみなら一時的に使ってOK）
        conn.execute(text("INSERT INTO messages (content) VALUES (:msg)"), {"msg": "Hello World"})
        
        # 最新のデータ1件を取得
        result = conn.execute(text("SELECT content FROM messages ORDER BY id DESC LIMIT 1"))
        message = result.scalar()

    return templates.TemplateResponse("index.html", {"request": request, "message": message})
