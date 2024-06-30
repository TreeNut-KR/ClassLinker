# -*- coding: utf-8 -*-
import requests
import json

cancel_url = 'https://apis.aligo.in/cancel/'

# ================================================================== 전송내역조회 필수 key값
# API key, userid, mid
# API키, 알리고 사이트 아이디, 메세지 고유ID	

cancel_data = {'key' : 'apikey',#api key 
               'userid' : 'aligo_id', # 알리고 사이트 아이디 
               'mid' : '메세지 고유 id'
}
cancel_response = requests.post(cancel_url, data=cancel_data)
print (cancel_response.json())
