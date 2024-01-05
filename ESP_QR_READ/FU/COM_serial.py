import serial
import serial.tools.list_ports as sp

list = sp.comports()
connected = []

## PC 연결된 COM Port 정보를 list에 넣어 확인한다.

for i in list:
    print(i)
    connected.append(i.device)
print("Connected COM ports: " + str(connected))
select_comport = input('select:')
ser = serial.Serial(select_comport, 9600, timeout = 0.2)

# 내가 연결할 Device의 명령어 delimiter가 Carrige return + Line Feed라고 하길래 delimeter를 설정해주었다.
while True:
    if ser.in_waiting > 0:  # 들어오는 데이터가 있는지 확인
        data = ser.readline().decode('utf-8').rstrip()  # 데이터 읽어오기