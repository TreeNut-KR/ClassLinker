# -*- coding: utf-8 -*-
import requests
import json

list_url ='https://apis.aligo.in/list/'

# ================================================================== 전송내역조회 필수 key값
# API key, userid
# API키, 알리고 사이트 아이디

list_data = {'key': 'apikey', #api key
            'userid': 'aligo_id', # 알리고 사이트 아이디 
            #'page' : '1', #페이지 번호 
            #'page_size' : '30', # 페이지당 출력갯수 (30~500)
            #'start_date' : 'YYYYMMDD', #조회시작일자
            #'limit_day' : 'YYYYMMDD' #조회마감일자
}
list_response = requests.post(list_url, data=list_data)
print(list_response.json())
