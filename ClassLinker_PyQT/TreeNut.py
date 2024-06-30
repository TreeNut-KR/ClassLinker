import os
import queue
import subprocess
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext

import requests
import serial
import serial.tools.list_ports as sp
from PIL import Image, ImageTk

# 암호와 실행할 명령어 설정
password = '0000'
command = 'chmod a+rw /dev/ttyUSB0'

# echo를 사용하여 암호를 sudo에 전달
cmd = f"echo {password} | sudo -S {command}"
subprocess.run(cmd, shell=True, text=True)

class SerialReader:
    def __init__(self, comport="COM3", baudrate=9600, timeout=0.2):  # /dev/ttyUSB0 or COM4
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
    def __init__(self):
        self.base_url = None
        self.session = requests.Session()

    def set_base_url(self, base_url):
        self.base_url = base_url

    def send_data(self, data):
        if not self.base_url:
            raise ValueError("Base IP is not set.")
        url = f"http://{self.base_url}:8100/qr"
        payload = {'qr_data': data}
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
            return response
        except requests.RequestException as e:
            return e


def mask_data(data):
    # 데이터를 받아서 첫 8글자를 제외한 나머지를 '*'로 변환
    return data[:8] + '*' * (len(data) - 8)


def read_serial_and_send(serial_reader, fastapi_client, text_area):
    while True:
        data = serial_reader.read_line()
        if data:
            masked_data = mask_data(data)
            text_area.insert(tk.END, f"Read data: {masked_data}\n", 'info')
            text_area.yview(tk.END)  # 자동 스크롤
            try:
                response = fastapi_client.send_data(data)
                if response.status_code == 200:
                    text_area.insert(tk.END, f"Success: {masked_data}\n", 'success')
                else:
                    text_area.insert(tk.END, f"Failed: {masked_data}, Status Code: {response.status_code}, Response: {response.text}\n", 'fail')
            except requests.ConnectionError:
                text_area.insert(tk.END, f"Failed: {masked_data}, Error: 정상적으로 연결되지 않았습니다.\n", 'fail')
            except requests.Timeout:
                text_area.insert(tk.END, f"Failed: {masked_data}, Error: 요청 시간이 초과되었습니다.\n", 'fail')
            except AttributeError as e:
                text_area.insert(tk.END, f"Failed: {masked_data}, Error: 정상적으로 연결되지 않았습니다.\n", 'fail')
            
            text_area.yview(tk.END)  # 자동 스크롤



def validate_ip(input_str):
    # 입력된 문자열이 숫자와 점(.)으로만 구성되었는지 확인
    return all(char.isdigit() or char == '.' for char in input_str)


def set_url(fastapi_client, url_entry, text_area):
    base_url = url_entry.get()
    fastapi_client.set_base_url(base_url)
    text_area.insert(tk.END, f"Base IP set to: {base_url}\n", 'info')
    text_area.yview(tk.END)  # 자동 스크롤


def setup_ui(fastapi_client):
    root = tk.Tk()
    root.title("TreeNut")  # 프로그램 이름 변경
    # 아이콘 파일 경로 설정
    icon_path = os.path.join(os.path.dirname(__file__), 'treenut.ico')
    
    # 아이콘 설정
    if os.path.exists(icon_path):
        try:
            img = ImageTk.PhotoImage(Image.open(icon_path))
            root.tk.call('wm', 'iconphoto', root._w, img)
        except Exception as e:
            print(f"Icon setting failed: {e}")
    else:
        print(f"Error: {icon_path} 파일을 찾을 수 없습니다.")
    # 창의 크기를 고정
    root.geometry("600x500")
    root.resizable(False, False)
    root.attributes("-fullscreen", False)
    root.minsize(400, 500)
    root.maxsize(400, 500)

    frame = tk.Frame(root)
    frame.pack(pady=10, padx=10)

    url_label = tk.Label(frame, text="Base IP:")
    url_label.pack(side=tk.LEFT)

    # validatecommand를 설정하여 IP 주소 검증
    validate_cmd = root.register(validate_ip)

    url_entry = tk.Entry(frame, width=30, validate="key", validatecommand=(validate_cmd, '%P'))
    url_entry.pack(side=tk.LEFT, padx=5)
    url_entry.insert(0, "192.168.0.16")  # 기본 IP 설정

    set_url_button = tk.Button(frame, text="Set IP", command=lambda: set_url(fastapi_client, url_entry, text_area))
    set_url_button.pack(side=tk.LEFT, padx=5)

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_area.pack(pady=10, padx=10)
    text_area.tag_config('success', foreground='green')
    text_area.tag_config('fail', foreground='red')
    text_area.tag_config('info', foreground='blue')
    return root, text_area


if __name__ == "__main__":
    serial_reader = SerialReader()
    fastapi_client = FastAPIClient()
    fastapi_client.set_base_url("192.168.0.16")  # 기본 IP 설정

    root, text_area = setup_ui(fastapi_client)

    reader_thread = Thread(target=read_serial_and_send, args=(serial_reader, fastapi_client, text_area), daemon=True)
    reader_thread.start()

    root.mainloop()
