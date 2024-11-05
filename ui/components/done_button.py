from PyQt5.QtWidgets import QPushButton

class DoneButton(QPushButton):
    def __init__(self, text, on_click):
        super().__init__(text)
        self.setStyleSheet("background-color: #3D5AFE; color: white; font-weight: bold; padding: 8px;")
        self.setFixedWidth(200)
        self.clicked.connect(on_click)
