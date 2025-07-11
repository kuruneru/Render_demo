from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import time
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:3306/{os.environ['DB_NAME']}"
engine = create_engine(DB_URL)

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


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello from MySQL'")).fetchone()
    return templates.TemplateResponse("index.html", {"request": request, "msg": result[0]})

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=port)

