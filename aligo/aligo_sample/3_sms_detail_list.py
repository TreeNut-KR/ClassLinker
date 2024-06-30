# -*- coding: utf-8 -*-
import requests
import json

detail_url ='https://apis.aligo.in/sms_list/'

# ================================================================== 전송내역조회 필수 key값
# API key, userid, mid
# API키, 알리고 사이트 아이디, 메세지 고유ID	

detail_data = {'key': 'apikey', #api key
            'userid': 'aligo_id', # 알리고 사이트 아이디 
            'mid' : '메세지 고유 ID',
            #'page' : '1', #페이지 번호 
            #'page_size' : '30' # 페이지당 출력갯수 (30~500)
}
detail_response = requests.post(detail_url, data=detail_data)
print(detail_response.json())
