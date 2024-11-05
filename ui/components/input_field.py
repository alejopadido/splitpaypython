from PyQt5.QtWidgets import QLineEdit

class InputField(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedWidth(200)
