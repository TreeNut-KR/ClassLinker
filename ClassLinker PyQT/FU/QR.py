import numpy as np
from pyzbar.pyzbar import decode

class QRcode_read:
    def __init__(self) -> None:
        self.qr_code_data = "가가가"

    def Decoding(self, frame):
        # QR 코드 디코딩
        decoded_objects = decode(frame)
        # 디코딩된 QR 코드가 있을 경우 처리
        for obj in decoded_objects:
            self.qr_code_data = obj.data.decode('utf-8')
            # QR 코드가 인식되면 루프를 종료합니다.
            return self.qr_code_data