# -*- coding: utf-8 -*-
import requests
import json

remain_url = 'https://apis.aligo.in/remain/'

# ================================================================== 발송가능건수 필수 key값
# API key, userid
# API키, 알리고 사이트 아이디

remain_data = {'key' : 'apikey',#api key 
               'userid' : 'aligo_id' # 알리고 사이트 아이디 
}
remiain_response = requests.post(remain_url, data=remain_data)
print (remiain_response.json())
