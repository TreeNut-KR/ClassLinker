# -*- coding: utf-8 -*-
import requests
import json

send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기

# ================================================================== 문자 보낼 때 필수 key값
# API key, userid, sender, receiver, msg
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

sms_data={'key': 'apikey', #api key
        'userid': 'aligo_id', # 알리고 사이트 아이디
        'sender': 'sender', # 발신번호
        'receiver': '01000000000', # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': '%고객명% test', #문자 내용 
        'msg_type' : 'msg_type', #메세지 타입 (MMS)
        'title' : 'title', #메세지 제목 (장문 및 그림문자에 적용)
        'destination' : '01000000000|홍길동'
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '', #테스트모드 적용 여부 Y/N
}

# 이미지 입력, 절대경로, 상대경로 상관없음.
files = {'image' : open('@이미지의 로컬 경로', 'rb')}

send_response = requests.post(send_url, data = sms_data, files = files)
print (send_response.json())
