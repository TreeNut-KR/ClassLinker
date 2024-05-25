from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator as field_validator
from typing import Optional, Tuple, Dict, Any
from dotenv import load_dotenv
from datetime import datetime
import ctypes
from ctypes.wintypes import MAX_PATH
import requests
import mysql.connector
import logging
import uvicorn
import os
from pathlib import Path
from sys import platform

MAX_PATH = 260
def get_documents_folder():
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    path_buf = ctypes.create_unicode_buffer(MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, path_buf)
    return path_buf.value

if platform == "linux" or platform == "linux2":
    documents_path = Path(__file__).parent.parent
elif platform == "win32":
    documents_path = Path(get_documents_folder())

log_file_path = documents_path / 'Aligo(JMEDU)_logs.log'
if not log_file_path.parent.exists():
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='a')

class QRdata(BaseModel):
    qr_data: str = Field(..., title="QR 코드",
                         description="학생 QR Code를 나타내는 문자열입니다. 36자리 값으로 설정해야됩니다.",)
    @field_validator('qr_data')
    def check_length(cls, v) -> str:
        if len(v) != 36:
            raise ValueError(f"QR Code는 정확히 36자리여야 합니다. 입력된 값의 길이: {len(v)}")
        return v

class QRresult(BaseModel):
    message: str = Field(..., title="메시지")
    qr_data: str = Field(..., title="QR 코드")
    parent_contact: str = Field(..., title="부모 전화번호")
    send_result: Any = Field(..., title="전송 결과")


class Aligo: 
    def __init__(self) -> None:
        load_dotenv()  # .env 파일 로드
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = "김준건"
        self.receiver_num = "0327667789"
        self.sms_data = {
            'key': os.getenv('SMS_KEY'),
            'userid': os.getenv('SMS_USERID'),
            'sender': os.getenv('SMS_SENDER'),
            'receiver': self.receiver_num,
            'msg_type': os.getenv('SMS_MSG_TYPE'),
            'title': os.getenv('SMS_TITLE'),
            'testmode_yn': os.getenv('SMS_TESTMODE_YN')
        }
        
    def send_sms(self, receiver_name: str, receiver_num: str) -> Tuple[str, str, str]:
        self.receiver_name = receiver_name
        self.sms_data['receiver'] = receiver_num
        # 메시지 포맷
        current_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        msg_template = (
            f"메시지 타입 {os.getenv('SMS_MSG_TYPE')}.\n"
            f"{self.receiver_name} JMEDU 테스트 메시지.\n"
            f"등원 시간 {current_time}"
        )
        
        # 기존 self.sms_data 복사 후 'msg'만 업데이트
        sms_data_updated = self.sms_data.copy()
        sms_data_updated['msg'] = msg_template
        
        send_response = requests.post(self.send_url, data=sms_data_updated)
        return send_response.json().get('message'), send_response.json().get('msg_type'), send_response.json().get('title')

load_dotenv()
db_config = {
    'host': os.getenv('MYSQL_ROOT_HOST'),
    'user': os.getenv('MYSQL_ROOT_USERDB_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': 3306
}
cnx = mysql.connector.connect(**db_config)

def get_parent_contact(QR: str) -> tuple:
    '''
    정상    : 학생 이름과 부모님 연락처를 반환 
    비정상  : 에러 메시지와 None 반환.
    '''
    try:
        with cnx.cursor() as cursor:
            query = "SELECT name, contact_parent FROM student WHERE student_pk = %s"
            cursor.execute(query, (QR,))
            result = cursor.fetchone()
            
        if result:
            return result[0], result[1]  # 정상적으로 학생 이름과 부모님 연락처를 반환
        else:
            return "해당 QR의 학생이 데이터베이스에 존재하지 않습니다.", None  # 에러 메시지와 None 반환
    except mysql.connector.Error as err:
        return f"데이터베이스 에러: {err}", None  # 에러 메시지와 None 반환

@app.post("/qr", response_model=QRresult, summary="QR Code 수신")
def receive_qr(request_data: QRdata) -> QRresult:
    '''
    출석 키호스크에서 QR코드를 전달 받아 Aligo Web 발신 후 
    성공 여부를 반환합니다.

    Args:\n\n
        qr_data (str): UUID

    예제 요청:
    {
        "qr_data": "3335caf1-198c-11ef-b8a7-0242c0a87002"
    }
    '''
    aligo_instance = Aligo()
    try:
        student_name, parent_contact = get_parent_contact(request_data.qr_data)
    
        if parent_contact is None:
            raise HTTPException(status_code=422, detail=f"{student_name}의 문자 수신 번호가 누락되었습니다.")
        else:
            send_result = aligo_instance.send_sms(student_name, parent_contact)
            logging.info(f'Received QR Data: {request_data.qr_data} '
                         f'Student\'s name: {student_name} '
                         f'Parent\'s Contact: {parent_contact} '
                         f'aligo: {send_result}')
            return QRresult(
                message="QR data and parent's contact received successfully",
                qr_data=request_data.qr_data,
                parent_contact=parent_contact,
                send_result=send_result
            )
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="서버에서 처리할 수 없는 요청입니다. 관리자에게 문의해주세요.")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)