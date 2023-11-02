import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

from FU.api import aligo
import FU.QR_new as QR

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def resizeEvent(self, event):
        # 창 크기가 변경될 때마다 비율을 유지하도록 계산
        size = self.size()
        if size.width() / size.height() > self.aspect_ratio:
            new_width = int(size.height() * self.aspect_ratio)
            self.resize(new_width, size.height())
        else:
            new_height = int(size.width() / self.aspect_ratio)
            self.resize(size.width(), new_height)

        x = self.geometry().width()
        y_1 = (3*x/5-0.5)/10
        y_2 = (x/4+3)/10

        state_font = QFont('GmarketSansTTFBold', round(y_1))
        state_font.setWeight(QFont.Bold)
        self.status_label.setFont(state_font)

        butt_font = QFont('GmarketSansTTFBold', round(y_2))
        butt_font.setWeight(QFont.Bold)
        self.in_button.setFont(butt_font)
        
        event.accept()
        
    def initUI(self):
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
        self.status_label = QLabel('Status: Not Recorded', text_box_frame)
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

        self.in_button.clicked.connect(self.record_in)

    def record_in(self):
        user = QR.main()
        QR.quit()
        self.api = aligo(user)
        try:
            text, found_name, msg_type = self.api.send_sms()
            self.status_label.setText(f'{found_name}<br>{msg_type} 보내기 {text.upper()}<br>{datetime.now().strftime("%m월 %d일 - %H:%M:%S")} 등원')
        except:
            pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AttendanceApp()
    ex.show()
    sys.exit(app.exec_())
