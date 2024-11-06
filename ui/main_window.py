from PyQt5.QtWidgets import QMainWindow
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.group_overview_screen import GroupOverviewScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay Navigation Example")

        # Initialize screens
        self.welcome_screen = WelcomeScreen()
        self.group_overview_screen = GroupOverviewScreen()

        # Set the initial screen
        self.setCentralWidget(self.welcome_screen)

        # Connect the signal from welcome_screen to a method to switch screens
        self.welcome_screen.navigate_to_group_overview.connect(self.show_group_overview)

    def show_group_overview(self):
        # Change the central widget to the group overview screen
        self.setCentralWidget(self.group_overview_screen)
