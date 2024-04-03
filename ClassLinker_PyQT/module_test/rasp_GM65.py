import serial
import serial.tools.list_ports
from typing import Union

class DeviceData:
    def ar_get(self, mod: str) -> Union[str, None]:
        """
        Arduino 데이터
        """
        ports = serial.tools.list_ports.comports()
        for port_get, _, _ in sorted(ports):
            if mod in port_get:
                return port_get
        return None
    
    def read_serial_data(self) -> str:
        '''
        아두이노에서 보낸 데이터를 data에 임시저장
        '''
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode().rstrip()
            return data

    def read(self, port: str) -> None:
        """
        지정된 포트로부터 데이터를 읽어서 출력
        """
        try:
            # 시리얼 연결 설정
            with serial.Serial(port, 9600) as self.ser:
                print(f"{port}에 연결되었습니다.")
                
                # 데이터 읽기
                while True:
                    if self.ser.in_waiting > 0:
                        line = self.read_serial_data()
                        print(line)
        except serial.SerialException as e:
            print(f"시리얼 포트 {port}에 연결하는 동안 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    df = DeviceData()
    port = df.ar_get("USB")
    
    if port:
        print(f"연결된 포트: {port}")
        df.read(port)
    else:
        print("USB로 연결된 장치를 찾을 수 없습니다.")
