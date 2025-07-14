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

@app.on_event("startup")
def startup():
    # アプリ起動時に 'Hello World' を1回だけINSERT（既にある場合はスキップ）
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM messages"))
        count = result.scalar()
        if count == 0:
            conn.execute(text("INSERT INTO messages (content) VALUES (:val)"), {"val": "Hello World"})
            conn.commit()

@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT content FROM messages ORDER BY id DESC LIMIT 1"))
        message = result.scalar()
    return templates.TemplateResponse("index.html", {"request": request, "message": message})
