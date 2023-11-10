import sys
import os
import cv2
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont, QFontDatabase, QKeyEvent
from PyQt5.QtCore import Qt

from FU.api import aligo
from FU.QR_new import QRcode_read
from FU.camera import Camera

class AttendanceApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.initUI()
        self.cam = Camera()
        print(self.cam.cameras_list)
        self.user = None

    def initUI(self) -> None:
        self.setWindowTitle('Attendance System')
        self.setGeometry(100, 100, 720, 1280)
        self.setMinimumSize(270, 480)
        self.aspect_ratio = 9 / 16  # 원하는 비율
        self.setStyleSheet("background-color: #01040A;")

        fontDB = QFontDatabase()
        font_dir = "./DATA/GmarketSansTTF/"
        font_files = [font_dir + file for file in os.listdir(font_dir) if file.endswith(".ttf")]
        for font in font_files:
            fontDB.addApplicationFont(font)
            
        state_font = QFont('GmarketSansTTFBold', 35)
        state_font.setWeight(QFont.Bold)
        butt_font = QFont('GmarketSansTTFBold', 15)
        butt_font.setWeight(QFont.Bold)
        
        text_box_frame = QFrame(self)
        self.status_label = QLabel('CLASS LINKER\nTEST', text_box_frame)
        self.status_label.setStyleSheet(
            "background-color: #0D1116;"
            "border: 1px solid #30363D;"
            "border-radius: 7px;"
            "color: #F0F6FC;"
            "padding: 6px;"
        )
        self.status_label.setFont(state_font)
        self.status_label.setAlignment(Qt.AlignCenter | Qt.AlignLeft)

        self.in_button = QPushButton('QR 인증')
        self.in_button.setStyleSheet(
            "background-color: #0D1116;"
            "border: 1px solid #30363D;"
            "border-radius: 7px;"
            "color: #F0F6FC;"
            "padding: 6px;"
        )
        self.in_button.setFont(butt_font)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.in_button)
        text_box_frame.setLayout(layout)
        self.setLayout(layout)

        self.in_button.clicked.connect(self.on_button_clicked)

    def toggle_fullscreen(self) -> None:
        screens = QApplication.screens()
        if len(screens) > 1:
            screen = screens[1]
            screen_geometry = screen.geometry()
            self.setGeometry(screen_geometry)
            self.showFullScreen()
        else:
            screen = screens[0]
            screen_geometry = screen.geometry()
            self.setGeometry(screen_geometry)
            self.showFullScreen()

    def resizeEvent(self, event: QKeyEvent) -> None:
        # 창 크기가 변경될 때마다 비율을 유지하도록 계산
        size = self.size()
        if size.width() / size.height() > self.aspect_ratio:
            new_width = int(size.height() * self.aspect_ratio)
            self.resize(new_width, size.height())
        else:
            new_height = int(size.width() / self.aspect_ratio)
            self.resize(size.width(), new_height)

        widget_list = [
            (self.status_label, 'GmarketSansTTFBold', (3*self.geometry().width()/5-0.5)/10 - 5),
            (self.in_button, 'GmarketSansTTFBold', (self.geometry().width()/4+3)/10)
        ]

        for widget, font_name, size in widget_list:
            font = QFont(font_name, round(size))
            font.setWeight(QFont.Bold)
            widget.setFont(font)
        event.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # F11 키를 누르면 전체 화면 모드를 활성화 / 비활성화
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
                self.setGeometry(100, 100, 720, 1280)
            else:
                self.toggle_fullscreen()
        # ESC 키를 누르면 전체 화면 모드를 해제
        elif event.key() == Qt.Key_Escape:
            self.showNormal()  # 전체 화면 해제
            self.setGeometry(100, 100, 720, 1280)

    @property
    def user(self) -> str: 
        return self._user
    
    @user.setter
    def user(self, code: str) -> None:
        self._user = code

    def on_button_clicked(self) -> None:
        self.record_in()
        self.api_use()

    def record_in(self) -> None:
        self.status_label.setText("인증 중")
        QR = QRcode_read()
        
        # 카메라가 연결되어 있는지 먼저 확인합니다.3
        if self.cam.cameras_list.items() is None:
            pass
        else:
            # 카메라를 열고 프레임을 계속 읽습니다.
            self.cam.open_camera()
            while True:
                try:
                    cv2.imshow('QR Code Reader', self.cam.frame)
                    self.user = QR.Decoding(self.cam.frame)

                    if self.user or (cv2.waitKey(1) & 0xFF == ord('q')):
                        break
                except:
                    break
                
        self.cam.release_camera()
        cv2.destroyAllWindows()

    def api_use(self) -> None:
        # self.user가 None인 경우에 대한 처리를 추가하였습니다.
        if self.user is None:
            self.status_label.setText("QR 코드를 읽지 못했습니다")
        else:
            self.api = aligo(self.user)
            try:
                text, found_name, msg_type = self.api.send_sms()
                self.status_label.setText(f'{found_name}<br>{msg_type} 보내기 {text.upper()}<br>{datetime.now().strftime("%m월 %d일 - %H:%M:%S")} 등원')
            except:
                self.status_label.setText("SMS 전송에 실패했습니다")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AttendanceApp()
    ex.show()
    sys.exit(app.exec_())
