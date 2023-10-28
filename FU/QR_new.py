import cv2
from pyzbar.pyzbar import decode

def main():
    # 웹 카메라 열기
    cap = cv2.VideoCapture(1)
    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if ret:
            try:
                # QR 코드 디코딩
                decoded_objects = decode(frame)
                # 디코딩된 QR 코드가 있을 경우 처리
                for obj in decoded_objects:
                    qr_code_data = obj.data.decode('utf-8')
                    # QR 코드가 인식되면 루프를 종료합니다.
                    return qr_code_data
                # 화면에 프레임 표시
                cv2.imshow('QR Code Reader', frame)
            except:
                pass 

            # 'q' 키를 누르면 루프를 종료합니다.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # 카메라 및 창 종료
    cap.release()
    cv2.destroyAllWindows()
def quit():
    cv2.destroyAllWindows()