import requests
import configparser
from typing import Tuple, Any, Dict

class aligo(): 
    def __init__(self, receiver_name: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./DATA/config.ini', encoding='utf-8')
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = receiver_name

    @property
    def sms_data(self) -> Dict[str, Any]:
        return self._sms_data
    
    @sms_data.setter
    def sms_data(self, value: configparser.ConfigParser) -> None:
        if not isinstance(value, configparser.ConfigParser):
            raise ValueError("sms_data는 반드시 configparser.ConfigParser 인스턴스여야 합니다.")
        
        required_keys = ['key', 'userid', 'sender', 'receiver', 'msg', 'msg_type', 'title', 'destination', 'testmode_yn']
        if not all(key in value['sms'] for key in required_keys):
            raise ValueError(f"{required_keys} 키가 configparser.ConfigParser 인스턴스에 반드시 포함되어야 합니다.")

        
        self._sms_data = {
            'key': value['sms']['key'],
            'userid': value['sms']['userid'],
            'sender': value['sms']['sender'],
            'receiver': value['sms']['receiver'],
            'msg': value['sms']['msg'],
            'msg_type': value['sms']['msg_type'],
            'title': value['sms']['title'],
            'destination': value['sms']['destination'],
            'testmode_yn': value['sms']['testmode_yn']
        }

    def send_sms(self) -> Tuple[str, str, str]:
        self.sms_data = self.config
        
        user = self.sms_data.get('destination')
        receiver_info = user.split(', ')
        receiver_dict = {info.split('|')[0]: 
                         info.split('|')[1] 
                         for info in receiver_info}
       
        if receiver_dict.get(self.sms_data.get('receiver')) == self.receiver_name:
            send_response = requests.post(self.send_url, data=self.sms_data)
            
            return send_response.json().get('message'), self.receiver_name, send_response.json().get('msg_type')
