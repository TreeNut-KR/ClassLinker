import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel  # Import QLabel
from FU.api import aligo
# from FU.QR import QRCode

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.api = aligo()

    def initUI(self):
        self.setWindowTitle('School Attendance System')
        self.setGeometry(100, 100, 400, 200)

        self.in_button = QPushButton('In', self)
        self.status_label = QLabel('Status: Not Recorded', self)  # Create QLabel

        layout = QVBoxLayout()
        layout.addWidget(self.in_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.in_button.clicked.connect(self.record_in)

    def record_in(self):
        self.status_label.setText('Status: In')
        # self.QR_Read = QRCode()
        # print(self.QR_Read)
        self.api.send_sms()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AttendanceApp()
    ex.show()
    sys.exit(app.exec_())
