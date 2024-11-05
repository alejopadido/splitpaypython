from PyQt5.QtWidgets import QLabel

class SubtitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("color: gray; font-size: 14px;")