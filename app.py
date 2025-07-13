from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv  # ← これを追加
import os

load_dotenv()  # ← .env ファイルの読み込み

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_url = os.getenv("DATABASE_URL")  # Noneになる原因はこれ
engine = create_engine(db_url, echo=True)

@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello World' AS message"))
        message = result.scalar()
    return templates.TemplateResponse("index.html", {"request": request, "message": message})
