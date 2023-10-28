import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from FU.api import aligo
import FU.QR_new as QR

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('School Attendance System')
        self.setGeometry(100, 100, 720, 1280)
        self.setStyleSheet("background-color: #01040A;")

        text_box_frame = QFrame(self)
        state_font = QFont('함초롬돋움', 35, QFont.Bold)
        butt_font = QFont('함초롬돋움', 14, QFont.Bold)

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
