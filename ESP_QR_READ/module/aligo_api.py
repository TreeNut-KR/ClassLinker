import requests
import configparser
from typing import Tuple, Any, Dict

class aligo(): 
    def __init__(self, receiver_name: str, receiver_num: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./DATA_ini/config.ini', encoding='utf-8')
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
        
        required_keys = ['key', 'userid', 'sender', 'msg', 'msg_type', 'title', 'testmode_yn']
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
