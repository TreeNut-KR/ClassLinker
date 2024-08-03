import os
import subprocess
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext
from dotenv import load_dotenv
from PIL import Image, ImageTk
from typing import Optional, Tuple

import requests
import serial
import serial.tools.list_ports as sp

def run_sudo_command(password: str, command: str) -> None:
    '''sudo 명령어를 실행합니다
    
    Args:
        password (str): sudo 비밀번호
        command (str): 실행할 명령어
    '''
    cmd = f"echo {password} | sudo -S {command}"
    subprocess.run(cmd, shell=True, text=True)

def create_env_file(dotenv_path: str) -> None:
    '''.env 파일을 생성합니다
    
    Args:
        dotenv_path (str): .env 파일 경로
    '''
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w', encoding='utf-8') as f:
            f.write("# ↓ Enter information about 'IP' & 'PORT' here.\n")
            f.write("IP=192.168.1.224\n")
            f.write("PORT=8100\n")

class SerialReader:
    def __init__(self, comport: str = "/dev/ttyUSB0", baudrate: int = 9600, timeout: float = 0.2) -> None:
        '''SerialReader 클래스 초기화 및 연결 설정'''
        self.comport = comport
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def connect(self) -> None:
        '''시리얼 포트 연결'''
        try:
            self.ser = serial.Serial(self.comport, self.baudrate, timeout=self.timeout)
        except Exception as e:
            print(f"Failed to connect to serial port: {e}")

    def read_line(self) -> Optional[str]:
        '''시리얼 포트에서 한 줄 읽기
        
        Returns:
            읽은 데이터 문자열 또는 None
        '''
        if self.ser and self.ser.in_waiting > 0:
            return self.ser.readline().decode().rstrip()
        return None

class FastAPIClient:
    def __init__(self, ip: str, port: int) -> None:
        '''FastAPIClient 클래스 초기화
        
        Args:
            ip (str): API의 기본 IP
            port (int): API의 포트 번호
        '''
        self.session = requests.Session()
        self.base_ip = ip
        self.port = port

    def send_data(self, data: str) -> Optional[requests.Response]:
        '''데이터를 FastAPI 서버에 전송
        
        Args:
            data (str): 전송할 데이터
        
        Returns:
            requests.Response: 서버의 응답
        '''
        if not self.base_ip:
            raise ValueError("Base IP is not set.")
        url = f"http://{self.base_ip}:{self.port}/qr"
        payload = {'qr_data': data}
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
            return response
        except requests.RequestException as e:
            print(f"Failed to send data to server: {e}")
            return None

    def test_connection(self) -> bool:
        '''FastAPI 서버에 연결 테스트
        
        Returns:
            bool: 연결 성공 여부
        '''
        url = f"http://{self.base_ip}:{self.port}/"
        try:
            response = self.session.get(url, timeout=5)  # 5초 타임아웃 설정
            if response.status_code == 404 and "detail" in response.json() and response.json()["detail"] == "Not Found":
                return True
            response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
            return True
        except requests.RequestException:
            return False

def mask_data(data: str) -> str:
    '''데이터를 받아서 첫 8글자를 제외한 나머지를 '*'로 변환
    
    Args:
        data (str): 원본 데이터 문자열
        
    Returns:
        str: 마스킹된 데이터 문자열
    '''
    return data[:8] + '*' * (len(data) - 8)

def read_serial_and_send(serial_reader: SerialReader, fastapi_client: FastAPIClient, text_area: scrolledtext.ScrolledText) -> None:
    '''시리얼 포트에서 데이터를 읽고 FastAPI 서버에 전송
    
    Args:
        serial_reader (SerialReader): 시리얼 리더 인스턴스
        fastapi_client (FastAPIClient): FastAPI 클라이언트 인스턴스
        text_area (ScrolledText): 텍스트 영역 인스턴스
    '''
    while True:
        data = serial_reader.read_line()
        if not data:
            continue  # 데이터가 없으면 루프의 시작으로 돌아감

        masked_data = mask_data(data)
        text_area.configure(state='normal')  # 텍스트 영역을 수정 가능하게 설정
        text_area.insert(tk.END, f"Read data: {masked_data}\n", 'info')
        text_area.yview(tk.END)  # 자동 스크롤
        text_area.configure(state='disabled')  # 텍스트 영역을 다시 읽기 전용으로 설정

        response = fastapi_client.send_data(data)
        text_area.configure(state='normal')
        if response and response.status_code == 200:
            text_area.insert(tk.END, f"Success: {masked_data}\n", 'success')
        else:
            text_area.insert(tk.END, f"Failed: {masked_data}\n", 'fail')
        text_area.yview(tk.END)
        text_area.configure(state='disabled')

def validate_ip(input_str: str) -> bool:
    '''입력된 문자열이 숫자와 점(.)으로만 구성되었는지 확인
    
    Args:
        input_str (str): 검증할 문자열
        
    Returns:
        bool: 유효성 검사 결과
    '''
    return all(char.isdigit() or char == '.' for char in input_str)

def setup_ui(ip: str, port: str, fastapi_client: FastAPIClient) -> Tuple[tk.Tk, scrolledtext.ScrolledText]:
    '''UI를 설정하고 초기화
    
    Args:
        ip (str): 기본 IP 주소
        port (str): 포트 번호
        fastapi_client (FastAPIClient): FastAPI 클라이언트 인스턴스
        
    Returns:
        tuple: Tkinter 루트와 텍스트 영역 인스턴스
    '''
    root = tk.Tk()
    root.title("TreeNut")  # 프로그램 이름 변경
    icon_path = os.path.join(os.path.dirname(__file__), 'treenut.ico')  # 아이콘 파일 경로 설정
    
    try:  # 아이콘 설정
        img = ImageTk.PhotoImage(Image.open(icon_path))
        root.tk.call('wm', 'iconphoto', root._w, img)
    except FileNotFoundError:
        print(f"Icon not found at path: {icon_path}")
    except Exception as e:
        print(f"Icon setting failed: {e}")
        
    # 창의 크기를 고정
    root.geometry("600x500")
    root.resizable(False, False)
    root.attributes("-fullscreen", False)
    root.minsize(400, 500)
    root.maxsize(800, 600)

    # IP 주소를 표시하는 라벨 추가
    ip_label = tk.Label(root, text=f"Connected to IP: {ip}:{port}", font=("Arial", 12))
    ip_label.pack(pady=10)
    
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
    text_area.pack(pady=10, padx=10)
    text_area.tag_config('success', foreground='green')
    text_area.tag_config('fail', foreground='red')
    text_area.tag_config('info', foreground='blue')
    text_area.pack(expand=True, fill=tk.BOTH)

    # 텍스트 영역을 읽기 전용으로 설정
    text_area.configure(state='disabled')

    return root, text_area

def test_connection_and_update_ui(fastapi_client: FastAPIClient, text_area: scrolledtext.ScrolledText) -> None:
    '''서버 연결 테스트 후 결과를 UI에 표시
    
    Args:
        fastapi_client (FastAPIClient): FastAPI 클라이언트 인스턴스
        text_area (ScrolledText): 텍스트 영역 인스턴스
    '''
    is_connected = fastapi_client.test_connection()
    text_area.configure(state='normal')
    if is_connected:
        text_area.insert(tk.END, "Connection to the server was successful.\n", 'success')
    else:
        text_area.insert(tk.END, "Failed to connect to the server within 5 seconds.\n", 'fail')
    text_area.configure(state='disabled')
    text_area.yview(tk.END)

def main() -> None:
    '''메인 함수 실행'''
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(script_dir, '.env')
    create_env_file(dotenv_path)
    load_dotenv(dotenv_path)
    ip = os.getenv("IP")
    port = os.getenv("PORT")

    if not validate_ip(ip):
        print("유효하지 않은 IP 주소입니다.")
        return

    fastapi_client = FastAPIClient(ip, int(port))
    serial_reader = SerialReader()

    root, text_area = setup_ui(ip, port, fastapi_client)

    # 별도의 스레드에서 시리얼 읽기 및 전송 실행
    thread = Thread(target=read_serial_and_send, args=(serial_reader, fastapi_client, text_area))
    thread.daemon = True
    thread.start()
    # 서버 연결 테스트 실행
    test_connection_and_update_ui(fastapi_client, text_area)
    root.mainloop()

if __name__ == "__main__":
    # sudo 명령어 실행
    run_sudo_command(password='0000', command='chmod a+rw /dev/ttyUSB0')
    main()
