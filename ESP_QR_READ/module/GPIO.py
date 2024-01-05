import queue
import time
import serial
import requests  # 서버로 POST 요청을 보내기 위한 라이브러리

class GPIO:
    def __init__(self) -> None:
        """
        CP210x UART to USB를 사용한 윈도우 환경
        """
        self.data = ""
        self.connected = []
        self.q = queue.Queue()  # 큐 생성
        try:
            self.ser = serial.Serial(
                port='/dev/ttyAMA0',  # 또는 '/dev/ttyAMA0'을 사용해보세요.
                baudrate=9600,
                timeout=0.2
            )
        except:
            print("GPIO 연결 불가")
        # requests Session 객체 생성
        self.session = requests.Session()
    
    def read(self):
        if self.ser.in_waiting > 0:
            self.data = self.ser.readline().decode('utf-8').rstrip()
            print(self.data)
            datas = self.data.split('\r')
            for data in datas:
                self.q.put(data)

    def send_data_to_server(self):
        url = 'http://localhost:5100/QR'
        headers = {'Content-Type': 'application/json'}
        if not self.q.empty():
            data = self.q.get()
            print(f'Read data: {data}')
            payload = {'qrcode': data}
            try:
                start_time = time.time()  # 시작 시간 측정
                response = self.session.post(url, json=payload, headers=headers)
                elapsed_time = time.time() - start_time  # 경과 시간 계산
                print(f'queue range: {self.q.qsize()}\nStatus Code: {response.status_code}, Response: {response.text}')
                print(f'Time taken from QR read to POST: {elapsed_time} seconds\n')  # 경과 시간 출력
            except:
                print("error")

if __name__ == "__main__":
    # GPIO 객체 생성 및 사용
    gpio = GPIO()
    while True:
        try:
            gpio.read() 
            # gpio.send_data_to_server()
        except:
            print("GPIO 연결 해제\n센서 연결 상태 확인 바람")
            
       
            
        
