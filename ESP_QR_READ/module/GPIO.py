import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',  # 또는 '/dev/ttyAMA0'을 사용해보세요.
    baudrate=9600,
    timeout=0.2
)

while True:
    if ser.in_waiting > 0:
        qr_code = ser.readline().decode('utf-8').rstrip()
        print("Read QR Code:", qr_code)
    time.sleep(0.1)
