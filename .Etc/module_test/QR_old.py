import cv2
from pyzbar.pyzbar import decode
from FU.camera import Camera
import numpy as np
from typing import List, Tuple
from collections import deque

class QRCodeEvent:
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def remove_handler(self, handler):
        self.handlers.remove(handler)
    
    def fire(self, qr_type, qr_data):
        for handler in self.handlers:
            handler(qr_type, qr_data)

class QRCode:
    def __init__(self):
        self.results: List[Tuple[str, str]] = []
        self.qr_event = QRCodeEvent()
    
    def __call__(self, frame) -> List[Tuple[str, str]]:
        qr_type = None
        qr_data = None
        try:
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_type = obj.type
                qr_data = obj.data.decode('utf-8')
                self.results.append((qr_type, qr_data))
                self.qr_event.fire(qr_type, qr_data)  # QR 코드 인식 시 이벤트 발생
        except:
            pass
        return self.results

def handle_qr_code(qr_type, qr_data):
    print(f"{qr_type} 인식됨: {qr_data}")   

def main():
    cam = Camera()
    cam.open_camera()
    last_qr_data = None
    brightness_factor = 0.5

    qr_code = QRCode()
    qr_code.qr_event.add_handler(handle_qr_code)  # QR 코드 인식 이벤트에 핸들러 추가

    while cam.is_camera_open():
        frame = cam.get_frame()
        frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)
        cv2.imshow('카메라 화면', frame)
        qr_results = qr_code(frame)
        
        if qr_results == [] or last_qr_data == qr_results[0][1]:
            pass
        else:
            last_qr_data = qr_results[0][1]
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release_camera()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
