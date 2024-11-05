from PyQt5.QtWidgets import QLabel

class TitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-size: 24px; color: #3D5AFE; font-weight: bold;")
