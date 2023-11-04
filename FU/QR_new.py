import cv2
from pyzbar.pyzbar import decode

from FU.camera import Camera

class QRcode_read:
    def __init__(self) -> None:
        self.cam = Camera()
        self.cam_list = self.cam.cameras_list()
        self.qr_code_data = "가가가"

    def main(self):
        if self.cam_list:
            print(self.cam_list)
            # 웹 카메라 열기
            self.cam.open_camera()
            while True:
                # 프레임 읽기
                frame = self.cam.get_frame()
                cv2.imshow('QR Code Reader', frame)
                try:
                    # QR 코드 디코딩
                    decoded_objects = decode(frame)
                    # 디코딩된 QR 코드가 있을 경우 처리
                    for obj in decoded_objects:
                        self.qr_code_data = obj.data.decode('utf-8')
                        # QR 코드가 인식되면 루프를 종료합니다.
                        return self.qr_code_data
                    # 화면에 프레임 표시
                except:
                    pass 
                # 'q' 키를 누르면 루프를 종료합니다.
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.quit()
                    break
                # 카메라 및 창 종료
            self.quit()
        else:
            return "ERROR : 카메라 연결 안됨"

    def quit(self):
        self.cam.release_camera()
        cv2.destroyAllWindows()