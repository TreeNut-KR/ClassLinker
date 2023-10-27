import cv2
from camera import Camera
from pyzbar.pyzbar import decode

cam = Camera()
cam.open_camera()

while cam.is_camera_open():
    frame = cam.get_frame()  # 프레임 가져오기

    # 화면에 프레임 표시
    cv2.imshow('카메라 화면', frame)

    # QR 코드 스캔
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        print(f'QR 코드 값: {data}')


    # 'q' 키를 누르면 루프를 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업이 끝나면 카메라와 윈도우를 해제
cam.release_camera()
cv2.destroyAllWindows()
