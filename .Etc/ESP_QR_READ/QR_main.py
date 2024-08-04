import serial
import serial.tools.list_ports as sp
import requests  # 서버로 POST 요청을 보내기 위한 라이브러리
import threading  # 별도의 스레드를 생성하기 위한 라이브러리

class GPIO:
    def __init__(self) -> None:
        """
        CP210x UART to USB를 사용한 윈도우 환경
        """
        self.list = sp.comports()
        self.connected = []
        for i in self.list:
            print(i)
            self.connected.append(i.device)
        # requests Session 객체 생성
        self.session = requests.Session()

    def select(self):
        print("Connected COM ports: " + str(self.connected))
        try:
            select_comport = input('select:')
            self.ser = serial.Serial(select_comport, 9600, timeout = 0.2)
        except:
            self.__init__()
            self.select()
        
    def read(self):
        if self.ser.in_waiting > 0:  # 들어오는 데이터가 있는지 확인
            data = self.ser.readline().decode('utf-8').rstrip()  # 데이터 읽어오기
            return data

    def send_data_to_server(self, data):
        # 서버의 URL
        url = 'http://localhost:5100/QR'  # Flask 서버의 URL로 수정해야 합니다.
        headers = {'Content-Type': 'application/json'}
        payload = {'qrcode': data}
        try:
            # 서버로 POST 요청 보내기
            response = self.session.post(url, json=payload, headers=headers)  # Session 객체 사용
            print(f'Status Code: {response.status_code}, Response: {response.text}')
        except requests.exceptions.ConnectionError as e:
            print("연결 오류: 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다")
        except Exception as e:
            print("기타 오류: ", e)

def check_data(gpio):
    while True:
        data = gpio.read()
        if data:
            print(f'Read data: {data}')
            gpio.send_data_to_server(data)

if __name__ == "__main__":
    # GPIO 객체 생성 및 사용
    gpio = GPIO()
    gpio.select()
    # 별도의 스레드를 생성하여 데이터 체크 함수를 비동기적으로 실행
    threading.Thread(target=check_data, args=(gpio,)).start()
