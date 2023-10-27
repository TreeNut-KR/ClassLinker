from typing import List, Tuple
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from camera import Camera

class QRCode:
    def __init__(self) -> None:
        self.results: List[Tuple[str, str]] = []  # 결과를 저장할 리스트
    
    def __call__(self, frame) -> List[Tuple[str, str]]:
        qr_type = None
        qr_data = None
        try:
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_type = obj.type
                qr_data = obj.data.decode('utf-8')
                self.results.append((qr_type, qr_data))
        except:
            pass
        return self.results

if __name__ == "__main__":
    cam = Camera()
    cam.open_camera()
    last_qr_data = None  # 이전에 인식한 QR 코드 데이터를 저장하는 변수 
    # 밝기를 조절하기 위해 모든 픽셀 값에 상수를 곱합니다.
    brightness_factor = 0.5  # 밝기를 낮추기 위한 상수 (0.5는 현재 밝기의 절반)

    while cam.is_camera_open():
        qr_code = QRCode()
        frame = cam.get_frame()  # 프레임 가져오기
        
        frame = np.clip(frame * brightness_factor, 0, 255).astype(np.uint8)

        # 화면에 프레임 표시
        cv2.imshow('카메라 화면', frame)
        qr_results = qr_code(frame)  # QR 코드를 호출하여 결과를 얻음
        if qr_results == [] or last_qr_data == qr_results[0][1]:
            pass
        else:
            print(f"타입 : {qr_results[0][0]}")
            print(f"값 : {qr_results[0][1]}")
            last_qr_data = qr_results[0][1]
            

        # 'q' 키를 누르면 루프를 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release_camera()
    cv2.destroyAllWindows()


