from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
import sqlite3
import os
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="D:\\Joffice\\ClassLinker\\ESP_QR_READ\\SER\\SER_FAST_api")

def save_qrcode_to_db(qrcode: str):
    directory = 'C:\\DB'
    if not os.path.exists(directory):
        os.makedirs(directory)
    db_name = 'qrcodes.db'
    db_path = os.path.join(directory, db_name)

    # SQLite 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블이 존재하지 않는 경우 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qrcodes (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            qrcode TEXT
        )
    ''')
    # 데이터 삽입
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO qrcodes (timestamp, qrcode) VALUES (?, ?)', (timestamp, qrcode))
    conn.commit()
    conn.close()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("FAST_index.html", {"request": request})

@app.post("/QR")
def post_qrcode(request: Request, qrcode: str = Form(...)):
    save_qrcode_to_db(qrcode)
    return templates.TemplateResponse("FAST_index.html", {"request": request, "qrcode": qrcode})

if __name__ == "__main__":
    uvicorn.run(app, host='192.168.0.20', port=5100)
