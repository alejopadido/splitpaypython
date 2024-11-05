from PyQt5.QtWidgets import QMainWindow
from ui.screens.welcome_screen import WelcomeScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay")

        # Load Welcome Screen
        self.welcome_screen = WelcomeScreen()
        self.setCentralWidget(self.welcome_screen)
