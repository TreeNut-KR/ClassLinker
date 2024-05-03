import os
import qrencode
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

class QRWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.resize(size, size)

class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR 코드 생성기")
        
        self.text_input = QLineEdit()
        self.generate_button = QPushButton("QR 생성")
        self.generate_button.clicked.connect(self.generate_qr)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("텍스트 입력:"))
        layout.addWidget(self.text_input)
        layout.addWidget(self.generate_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.qr_window = QRWindow()  # qr_window를 인스턴스 변수로 선언
        
    def generate_qr(self):
        text = self.text_input.text()
        if text:
            # version 인자를 제거하거나 None으로 설정
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
                
            folder_path = "QR_FILE"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            file_path = os.path.join(folder_path, "qr_code.png")
            qr_image.save(file_path)
            
            # QR 코드 이미지를 새 창으로 띄우기
            self.qr_window.setWindowTitle("QR 코드")
            qr_label = QLabel(self.qr_window)
            qr_pixmap = QPixmap(file_path)
            qr_label.setPixmap(qr_pixmap)
            qr_label.setScaledContents(True)  # QLabel의 내용을 QLabel의 크기에 맞게 스케일링
            self.qr_window.setCentralWidget(qr_label)
            self.qr_window.show()
            
            print("QR 코드 생성 및 저장 완료!")
        else:
            print("텍스트를 입력해주세요.")

if __name__ == "__main__":
    app = QApplication([])
    window = QRCodeGenerator()
    window.show()
    app.exec_()
 