from api import aligo

receiver_name = '서정훈'  # 테스트하려는 수신자의 이름
aligo_instance = aligo(receiver_name)

# SMS를 보냅니다.
response_message, receiver, msg_type = aligo_instance.send_sms()

# 결과 출력
print(f"수신자: {receiver}")
print(f"메시지 유형: {msg_type}")
print(f"응답 메시지: {response_message}")