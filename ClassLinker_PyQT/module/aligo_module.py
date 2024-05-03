import requests
import configparser
from typing import Tuple, Any, Dict

class aligo(): 
    def __init__(self, receiver_name: str, receiver_num: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./ClassLinker_PyQT/DATA_ini/config.ini', encoding='utf-8')
        
        # 로드된 섹션들 확인
        print("로드된 섹션들:", self.config.sections())
        
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = receiver_name
        self.receiver_num = receiver_num

    @property
    def sms_data(self) -> Dict[str, Any]:
        return self._sms_data
    
    @sms_data.setter
    def sms_data(self, value: configparser.ConfigParser) -> None:
        if not isinstance(value, configparser.ConfigParser):
            raise ValueError("sms_data는 반드시 configparser.ConfigParser 인스턴스여야 합니다.")
        
        required_keys = ['SMS_KEY', 'SMS_USERID', 'SMS_SENDER', 'SMS_MSG', 'SMS_MSG_TYPE', 'SMS_TITLE', 'SMS_TESTMODE_YN']
        if not all(key in value['sms'] for key in required_keys):
            raise ValueError(f"{required_keys} 키가 configparser.ConfigParser 인스턴스에 반드시 포함되어야 합니다.")

        self._sms_data = {
            'key': value['sms']['SMS_KEY'],
            'userid': value['sms']['SMS_USERID'],
            'sender': value['sms']['SMS_SENDER'],
            'receiver': self.receiver_num,
            'msg': value['sms']['SMS_MSG'],
            'msg_type': value['sms']['SMS_MSG_TYPE'],
            'title': value['sms']['SMS_TITLE'],
            'testmode_yn': value['sms']['SMS_TESTMODE_YN']
        }

    def send_sms(self) -> Tuple[str, str, str]:
        self.sms_data = self.config
        send_response = requests.post(self.send_url, data=self.sms_data)

        return send_response.json().get('message'), self.receiver_name, send_response.json().get('msg_type')

# 서정훈 님에게 테스트 문자 보내기
receiver_name = "김동혁"
receiver_num = "01076127155"

# aligo 클래스의 인스턴스 생성
aligo_instance = aligo(receiver_name, receiver_num)
# 문자 메시지 전송
send_result = aligo_instance.send_sms()

# 전송 결과 출력
print(send_result)
