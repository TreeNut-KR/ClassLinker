
import requests
import configparser

class aligo(): 
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./DATA/config.ini', encoding='utf-8')
        self.send_url = 'https://apis.aligo.in/send/'

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
        send_response = requests.post(self.send_url, data=sms_data)
        print (send_response.json())