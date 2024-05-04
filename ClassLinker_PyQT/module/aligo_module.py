import requests
from typing import Tuple
from datetime import datetime
from dotenv import load_dotenv
import os

class aligo: 
    def __init__(self, receiver_name: str, receiver_num: str) -> None:
        load_dotenv('./ClassLinker_PyQT/DATA_env/.env')  # .env 파일 로드
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = receiver_name
        self.receiver_num = receiver_num
        
    def send_sms(self) -> Tuple[str, str, str]:
        # 메시지 포맷
        current_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        msg_template = (
            f"{self.receiver_name} JMEDU TEST message.\n"
            f"Current time is {current_time}\n"
            f"Message type is {os.getenv('SMS_MSG_TYPE')}."
        )
        
        sms_data = {
            'key': os.getenv('SMS_KEY'),
            'userid': os.getenv('SMS_USERID'),
            'sender': os.getenv('SMS_SENDER'),
            'receiver': self.receiver_num,
            'msg': msg_template,
            'msg_type': os.getenv('SMS_MSG_TYPE'),
            'title': os.getenv('SMS_TITLE'),
            'testmode_yn': os.getenv('SMS_TESTMODE_YN')
        }
        
        send_response = requests.post(self.send_url, data=sms_data)
        return send_response.json().get('message'), self.receiver_name, send_response.json().get('msg_type')

if __name__ == "__main__":
    # 서정훈 님에게 테스트 문자 보내기
    receiver_name = "서정훈"
    receiver_num = "01080091358"

    # aligo 클래스의 인스턴스 생성
    aligo_instance = aligo(receiver_name, receiver_num)
    # 문자 메시지 전송
    send_result = aligo_instance.send_sms()

    # 전송 결과 출력
    print(send_result)
