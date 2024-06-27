import queue
import socket

import requests
import serial
import serial.tools.list_ports as sp
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Display")
        self.setGeometry(100, 100, 400, 200)

        self.local_ip_label = QLabel()
        self.external_ip_label = QLabel()
        self.qr_data_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.local_ip_label)
        layout.addWidget(self.external_ip_label)
        layout.addWidget(self.qr_data_label)

        self.setLayout(layout)

        self.update_ip_addresses()

    def update_ip_addresses(self):
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        # Get external IP address
        external_ip = requests.get("https://api.ipify.org").text

        self.local_ip_label.setText(f"Local IP: {local_ip}")
        self.external_ip_label.setText(f"External IP: {external_ip}")

    def update_qr_data(self, data):
        # Display only the first and last 3 characters of the QR data
        displayed_data = data[:3] + "..." + data[-3:]
        self.qr_data_label.setText(f"QR Data: {displayed_data}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    serial_reader = SerialReader()
    fastapi_client = FastAPIClient("http://192.168.219.105:8000/qr")

    while True:
        data = serial_reader.read_line()
        if data:
            print(data)
            fastapi_client.send_data(data)
            window.update_qr_data(data)
        app.processEvents()
