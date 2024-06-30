# -*- coding: utf-8 -*-
import requests
import json

mass_send_url = 'https://apis.aligo.in/send_mass/' 


# ================================================================== 대량 문자 보낼 때 필수 key값
# API key, userid, sender, rec_1, msg_1, cnt, msg_type	
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용, 메세지 전송건수, [SMS(단문) , LMS(장문), MMS(그림문자) 구분]	

sms_data={'key': 'apikey', #api key
        'userid': 'aligo_id', # 알리고 사이트 아이디
        'sender': 'sender', # 발신번호
        'rec_1': '01000000000', # 수신자 전화번호1	
        'msg_1': 'test_0', #메시지 내용1
        'rec_2': '01011111111', # 수신자 전화번호2	
        'msg_2': 'test_1', #메시지 내용2
        'cnt' : 2, #메세지 전송건수(번호,메세지 매칭건수)
        'title' : 'title', #메세지 제목 (장문 및 그림문자에 적용)
        'msg_type' : 'msg_type', #메세지 타입 (SMS, LMS, MMS)
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
}
mass_send_response = requests.post(mass_send_url, data=sms_data)

print (mass_send_response.json())
