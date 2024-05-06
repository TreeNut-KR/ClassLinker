import requests
from typing import Tuple
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import uvicorn
import os

app = FastAPI()

class QRData(BaseModel):
    qr_data: str

class jmedu_db:
    def __init__(self) -> None:
        load_dotenv("./ClassLinker_PyQT/DB_env/.env") 
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT')  # 포트는 문자열로 저장되어 있어야 합니다
        }
        self.cnx = mysql.connector.connect(**self.db_config)

    def get_parent_contact(self, student_name: str) -> tuple:
        '''
        정상    : 학생 이름과 부모님 연락처를 반환 
        비정상  : 에러 메시지와 None 반환.
        '''
        try:
            with self.cnx.cursor() as cursor:
                query = "SELECT name, contact_parent FROM student WHERE student_pk = %s"
                cursor.execute(query, (student_name,))
                result = cursor.fetchone()
                
            if result:
                return result[0], result[1]  # 정상적으로 학생 이름과 부모님 연락처를 반환
            else:
                return "해당 QR의 학생이 데이터베이스에 존재하지 않습니다.", None  # 에러 메시지와 None 반환
        except mysql.connector.Error as err:
            return f"데이터베이스 에러: {err}", None  # 에러 메시지와 None 반환

class Aligo: 
    def __init__(self) -> None:
        load_dotenv('./ClassLinker_PyQT/DATA_env/.env')  # .env 파일 로드
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = "서정훈"
        self.receiver_num = "01080091358"
        self.sms_data = {
            'key': os.getenv('SMS_KEY'),
            'userid': os.getenv('SMS_USERID'),
            'sender': os.getenv('SMS_SENDER'),
            'receiver': self.receiver_num,  # 수신자 번호는 초기화 시 설정
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

@app.post("/qr")
def receive_qr(qr_data: QRData):
    db_instance = jmedu_db()
    aligo_instance = Aligo()  # 클래스 이름과 다른 인스턴스 이름 사용
    student_name, parent_contact = db_instance.get_parent_contact(qr_data.qr_data)
    
    if parent_contact is None:
        return {"message": "Error", "data": student_name}
    else:
        send_result = aligo_instance.send_sms(student_name, parent_contact)
        print(
            f'''
            Received QR Data: {qr_data.qr_data} 
            Student's name: {student_name}
            Parent's Contact: {parent_contact}
            aligo: {send_result}
            '''
        )
        return {
            "message": "QR data and parent's contact received successfully",
            "data": qr_data.qr_data,
            "parent_contact": parent_contact,
            "send_result": send_result
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # jmedu_db = jmedu_db()
    # # Example of using the function
    # student_name = input("QR코드 : ")
    # parent_contact = jmedu_db.get_parent_contact(student_name)
    # print(f"{student_name}의 부모님 연락처: {parent_contact}")

    # # aligo 클래스의 인스턴스 생성
    # aligo_instance = aligo(receiver_name, receiver_num)
    # # 문자 메시지 전송
    # send_result = aligo_instance.send_sms()
    # # 전송 결과 출력
    # print(aligo_instance) 
    # print(send_result)
