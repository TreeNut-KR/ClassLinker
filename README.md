![transparent](https://capsule-render.vercel.app/api?type=transparent&fontColor=A991E5&text=CLASS%20LINKER&height=150&fontSize=60&desc=By%20Joffice%20:%20Kim,%20Seo,%20Goe&descAlignY=75&descAlign=60)


## 23.10.28. 
 기능 | 내용 
:--:|:---
`QR` | OpenCV, pyzbar를 이용, QR 리더기 구매 전까지 카메라로 QRCode를 decode 통해 인식 
`UI` | 임시로 PyQT5 상태 레이블과 QR 인식 버튼 구성
`API` | 버튼 클릭 시 유저 이름과 QR코드 대조 후 일치하면 SMS 전송 </br> -> 서버 구축 완료 시 QR코드를 서버 userID 대조하여 SMS 전송으로 변경

## 23.11.11. 
 기능 | 내용 
:--:|:---
`QR` | 카메라 연결 상태에 따라 UI에 상태 표시 </br> camera.py를 QR.py에서 분리하여 개별 모듈로 변경
`UI` | 창 비율 (**9:16**), 최소 크기 (**270x480**)으로 고정 및 창 크기에 따라 폰트 크기를 자동 조절 </br> F11로 전체화면 기능 추가 (ESC 또는 F11을 누르면 전체화면 해제) </br> 데코레이터를 사용하여 user 전달하도록 수정, 전체적인 코드 구조 변경 (QR에서 사용하던 코드 UI (*main.py)로 편입)
`API` | 데코레이터를 사용하여 sms_data 전달하도록 수정
`DATA` | api에 사용되는 ini 파일 제외 
`CAM` | 데코레이터를 사용하여 frame과 cam_list 전달하도록 수정, 전체적인 코드 구조 변경
