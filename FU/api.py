import requests
import configparser

class aligo(): 
    def __init__(self, receiver_name):
        self.config = configparser.ConfigParser()
        self.config.read('./DATA/config.ini', encoding='utf-8')
        self.send_url = 'https://apis.aligo.in/send/'
        self.receiver_name = receiver_name

    # send sms message
    def send_sms(self):
        sms_data = {
            'key': self.config['sms']['key'],
            'userid': self.config['sms']['userid'],
            'sender': self.config['sms']['sender'],
            'receiver': self.config['sms']['receiver'],
            'msg': self.config['sms']['msg'],
            'msg_type': self.config['sms']['msg_type'],
            'title': self.config['sms']['title'],
            'destination': self.config['sms']['destination'],
            'testmode_yn': self.config['sms']['testmode_yn']
        }

        user = sms_data.get('destination')
        receiver_info = user.split(', ')
        receiver_dict = {info.split('|')[0]: info.split('|')[1] for info in receiver_info}
        if receiver_dict.get(sms_data.get('receiver')) == self.receiver_name:
            send_response = requests.post(self.send_url, data=sms_data)
            return send_response.json().get('message'), self.receiver_name, send_response.json().get('msg_type')