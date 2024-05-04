import requests
import serial
import serial.tools.list_ports as sp
import queue

class SerialReader:
    def __init__(self, comport="/dev/ttyUSB0", baudrate=9600, timeout=0.2):
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
    fastapi_client = FastAPIClient("http://localhost:8000/qr")

    while True:
        data = serial_reader.read_line()
        if data:
            print(data)
            fastapi_client.send_data(data)
