import ctypes
import logging
import os
from ctypes.wintypes import MAX_PATH
from datetime import datetime
from pathlib import Path
from sys import platform
from typing import Any, Optional, Tuple, Union

import mysql.connector
import mysql.connector.cursor
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

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
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "qr_data": "3335cf9b-198c-11ef-b8a7-0242c0a87002"
                }
            ]
        }
    }

class QRresult(BaseModel):
    message: str = Field(..., title="메시지")
    student_name: Optional[str] = Field(None, title="학생 이름")
    send_result: Optional[Any] = Field(None, title="전송 결과")

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
        
    def send_sms(self, receiver_name: str, receiver_num: str, status: str) -> Tuple[str, str, str]:
        '''
        반환값 => (결과 : str, 문자 유형 : str, 타이틀 : str)
        '''
        self.receiver_name = receiver_name
        self.sms_data['receiver'] = receiver_num
        current_time = datetime.now().strftime('%H시 %M분')
        # 메시지 포맷
        msg_template = (
            "안녕하세요. 제이엠에듀 학원입니다.\n\n"
            f"금일 {current_time}, {self.receiver_name} 학생이\n"
            f"{status} 하였습니다.")
        # f"[제이엠에듀 출석시스템]\n"
        # f"■ 성명: {self.receiver_name}\n"
        # f"■ 시간: {current_time}\n"
        # f"■ 등·하원: {status}"
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

def procedure_attendance_contact(QR: str, cursor: mysql.connector.cursor) -> Union[Tuple[str, str, str], str]:
    ''' 반환값 => (번호 : str, 이름 : str, 상태 : str) : tuple'''
    try:

        cursor.callproc('RecordAttendance', (QR,))
        result_set = next(cursor.stored_results())  # 첫 번째 결과 집합에 직접 접근
        fetched_result = result_set.fetchone()
            
        if fetched_result:
            return fetched_result
        else:
            return "해당 QR의 학생이 데이터베이스에 존재하지 않습니다."  # 에러 메시지
        
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        raise HTTPException(status_code=500, detail="해당 QR의 학생이 데이터베이스에 존재하지 않습니다.")
            
@app.post("/qr", response_model=QRresult, summary="QR Code 수신")
def receive_qr(request_data: QRdata) -> QRresult:
    """
    출석 키호스크에서 QR코드를 전달 받아 Aligo Web 발신 후 성공 여부를 반환합니다.
    """
    try:
        cnx = mysql.connector.connect(**db_config)
        with cnx.cursor() as cursor:
            contact_result = procedure_attendance_contact(request_data.qr_data, cursor)
            cnx.commit()
        if isinstance(contact_result, str):
            logging.error(contact_result)
            return QRresult(message=contact_result)
        
        number, name, status = contact_result
        if status == "leave":
            logging.error(f"{name} 하원이 완료된 상태")
            return QRresult(message="금일 하원이 이미 완료되었습니다.", student_name=name)
        elif status == "wait":
            return QRresult(message="대기 중입니다. 수업이 끝난 뒤 다시 시도해주세요.", student_name=name)
        elif status == "attend":
            attendance_status = "등원"
        elif status == "already":
            attendance_status = "하원"
            
        try:
            message, msg_type, title = Aligo().send_sms(receiver_name=name, receiver_num=number, status=attendance_status)
            
            logging.info(f'Received QR Data: {request_data.qr_data} '
                        f'Student\'s name: {name} '
                        f'Parent\'s Contact: {number} '
                        f'status: {status}'
                        f'aligo: {message, msg_type, title}')
            return QRresult(message=f"{status}: {message}", student_name=name, send_result=msg_type)
        except Exception as e:
            
            cnx.rollback() # 전송 실패 시 attendance_log 롤백
            logging.error(f'An error occurred while sending SMS: {str(e)}')
            raise HTTPException(status_code=503, detail="문자 전송 할 수 없는 요청입니다. 관리자에게 문의해주세요.")
        
    except ValueError as ve:
        logging.error(f'An value error occurred: {str(ve)}')
        raise HTTPException(status_code=422, detail="입력된 데이터가 올바르지 않습니다.")
    except mysql.connector.Error as err:
        logging.error(f"등원 기록 중 데이터베이스 오류: {err}")
        raise HTTPException(status_code=503, detail="등원 기록 중 오류가 발생했습니다. 관리자에게 문의해주세요.")
    except UnboundLocalError as ue:
        logging.error(f'Unbound Local Error occurred: {str(ue)}')
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다. 관리자에게 문의해주세요.")
    except Exception as e:
            logging.error(f'An error occurred: {str(e)}')
            raise HTTPException(status_code=500, detail="서버에서 처리할 수 없는 요청입니다. 관리자에게 문의해주세요.")
    finally:
        if cnx.is_connected():
            cnx.close()
    
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)