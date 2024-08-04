import cv2
from pyzbar.pyzbar import decode

def scan_qr_code(video_capture):
    while True:
        ret, frame = video_capture.read()
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            print('Type: ', obj.type)
            print('Data: ', obj.data, '\n')
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture = cv2.VideoCapture(0)
scan_qr_code(video_capture)
video_capture.release()
cv2.destroyAllWindows()
