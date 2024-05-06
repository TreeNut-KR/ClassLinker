import serial
import serial.tools.list_ports as sp

def calculate_crc_ccitt(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
            crc &= 0xFFFF
    return crc

class GPIO:
    def __init__(self):
        """
        CP210x UART to USB를 사용한 환경
        """
        self.list = sp.comports()
        self.connected = [i.device for i in self.list]
        print("Connected COM ports:", self.connected)
        self.ser = None

    def connect(self, port="/dev/ttyUSB0", baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.2)
            print(f"{port}에 성공적으로 연결되었습니다.")
        except serial.SerialException as e:
            print(f"{port}에 연결 실패: {e}")

    def write_zone_bit(self, address, data):
        head = [0x7E, 0x00]  # Head
        types = [0x08]  # Types
        lens = [len(data)]  # Lens: 데이터 길이 (1 바이트), 예에서는 1
        address_bytes = [(address >> 8) & 0xFF, address & 0xFF]  # Address: 시작 위치
        crc_input = head + types + lens + address_bytes + data
        crc = calculate_crc_ccitt(crc_input)  # CRC 계산
        crc_bytes = [(crc >> 8) & 0xFF, crc & 0xFF]  # CRC 바이트
        full_command = crc_input + crc_bytes  # 전체 명령 구성
        self.ser.write(bytearray(full_command))  # 시리얼 포트를 통해 명령 전송
        print(f"Sent: {' '.join(f'{x:02X}' for x in full_command)}")  # 전송된 명령 출력


# 사용 예시
if __name__ == "__main__":
    gpio = GPIO()
    gpio.connect()  # 시리얼 포트를 올바르게 설정하세요.
    # LED를 끄기 위해 주소 0x0000에 데이터 0x00을 저장
    while 1:
        gpio.write_zone_bit(0x0000, [0x00])

