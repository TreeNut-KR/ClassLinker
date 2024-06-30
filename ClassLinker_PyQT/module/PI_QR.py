import requests
import serial
import serial.tools.list_ports as sp
import queue
import subprocess

# 암호와 실행할 명령어 설정
password = '0000'
command = 'chmod a+rw /dev/ttyUSB0'

# echo를 사용하여 암호를 sudo에 전달
cmd = f"echo {password} | sudo -S {command}"
subprocess.run(cmd, shell=True, text=True)

class SerialReader:
    def __init__(self, comport="COM4", baudrate=9600, timeout=0.2): #/dev/ttyUSB0
        self.comport = comport
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(self.comport, self.baudrate, timeout=self.timeout)
        except Exception as e:
            print(e)

    def read_line(self):
        if self.ser and self.ser.in_waiting > 0:
            return self.ser.readline().decode().rstrip()
        return None

class FastAPIClient:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def send_data(self, data):
        payload = {'qr_data': data}
        response = self.session.post(self.url, json=payload)
        print("Data sent to FastAPI:", response.text)

if __name__ == "__main__":
    serial_reader = SerialReader()
    fastapi_client = FastAPIClient("http://192.168.219.105:8000/qr")

    while True:
        data = serial_reader.read_line()
        if data:
            print(data)
            fastapi_client.send_data(data)
