![transparent](https://capsule-render.vercel.app/api?type=transparent&fontColor=A991E5&text=CLASS%20LINKER&height=150&fontSize=60&desc=By%20Joffice%20:%20Kim,%20Seo,%20Goe&descAlignY=75&descAlign=60)

## 23.10.28. 
 기능 | 내용 
:--:|:---
`QR` | OpenCV, pyzbar를 이용, QR 리더기 구매 전까지 카메라로 QRCode를 decode 통해 인식 
`UI` | 임시로 PyQT5 상태 레이블과 QR 인식 버튼 구성
`API` | 버튼 클릭 시 유저 이름과 QR코드 대조 후 일치하면 SMS 전송 </br> -> 서버 구축 완료 시 QR코드를 서버 userID 대조하여 SMS 전송으로 변경

## 23.11.05. 
 기능 | 내용 
:--:|:---
`UI` | 최소 창 크기를 (**270x480**)으로 고정 </br> 창 비율을 (**9:16**)으로 고정 </br> 창 크기에 따라 폰트 크기를 자동 조절 </br> F11로 전체화면 기능 추가 (ESC 또는 F11을 누르면 전체화면 해제)
`QR` | 카메라 연결 상태에 따라 UI에 상태 표시 </br> camera.py 모듈 QR_new.py에 적용