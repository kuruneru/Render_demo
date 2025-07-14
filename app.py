from fastapi import FastAPI, Request, Form
from sqlalchemy import create_engine, text
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, echo=True)

# indexページ表示（全メッセージを出力）
@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT content FROM messages ORDER BY id DESC"))
        messages = [row[0] for row in result.fetchall()]
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})

# フォームのPOST受け取り → SQLにINSERT
@app.post("/submit")
def submit_message(message: str = Form(...)):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO messages (content) VALUES (:msg)"), {"msg": message})
    return RedirectResponse("/", status_code=303)  # リダイレクトで更新
