from selenium import webdriver
from selenium.webdriver.edge import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from ESP_QR_READ.module.aligo_api import aligo

user_dict = {'012030831':'서정훈', '911378837':'김준건', '784981354':'고범준'}
user_num_dict = {'서정훈': '01080091358', '김준건':'01072821097', '고범준':'01025997894'}

qrcode_text = ""
# 옵션 설정
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.use_chromium = True
options.add_experimental_option("detach", True)

# Edge 파일 위치 설정
options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge Dev\\Application\\msedge.exe"
s = service.Service(r"msedgedriver.exe")

# Edge 드라이버 생성
driver = webdriver.Edge(options=options, service=s)
driver.get('http://222.100.190.53:5100/')

# WebDriverWait를 사용하여 qrcode 요소의 값을 주기적으로 확인
wait = WebDriverWait(driver, 10)  # 최대 10초 동안 대기
qrcode_element = driver.find_element(By.ID, 'qr-code')

while True:
    try:
        if qrcode_text != qrcode_element.text:
            qrcode_text = qrcode_element.text
            receiver_name = user_dict.get(qrcode_text)
            receiver_num = user_num_dict.get(receiver_name)
            if receiver_name is None:
                print("해당 사용자는 서버에 등록되지 않았습니다.")
                continue
            qrcode_text = qrcode_element.text
            # qrcode 요소의 텍스트 값을 가져옵니다.
            print("QR Code Value:", qrcode_text, "QR Code user:", receiver_name)
            aligo_instance = aligo(receiver_name, receiver_name)
            # SMS를 보냅니다.
            response_message, receiver, msg_type = aligo_instance.send_sms()
            # 결과 출력
            print(f"수신자: {receiver}")
            print(f"메시지 유형: {msg_type}")
            print(f"응답 메시지: {response_message}")
        time.sleep(1)
    
    except Exception as e:
        print("Error:", str(e))
        break
# 드라이버 종료
driver.quit()
