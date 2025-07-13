from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from starlette.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, echo=True)

@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello World' AS message"))
        message = result.scalar()
    return templates.TemplateResponse("index.html", {"request": request, "message": message})
