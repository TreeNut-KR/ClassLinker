from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
from datetime import datetime

class JMS_api:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="D:\\Joffice\\ClassLinker\\ESP_QR_READ\\SER\\SER_FAST_api")
        self.app.mount("/static", StaticFiles(directory="D:\\Joffice\\ClassLinker\\ESP_QR_READ\\SER\\SER_FAST_api"), name="static")
        self.setup_routes()

    def setup_routes(self):
        self.app.get("/")(self.GET) 
        self.app.post("/QR")(self.POST) 

    def save_qrcode_to_db(self, qrcode: str):
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

    async def GET(self, request: Request):
        return self.templates.TemplateResponse("FAST_index.html", {"request": request})

    async def POST(self, request: Request, qrcode: str = Form(...)):
        self.save_qrcode_to_db(qrcode)
        return self.templates.TemplateResponse("FAST_index.html", {"request": request, "qrcode": qrcode})