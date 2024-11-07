from PyQt5.QtWidgets import QMainWindow
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.group_overview_screen import GroupOverviewScreen
from ui.screens.create_bill_screen import CreateBillScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay Navigation Example")

        # Initialize screens
        self.welcome_screen = WelcomeScreen()
        self.group_overview_screen = GroupOverviewScreen()
        self.create_bill_screen = CreateBillScreen()

        # Set the initial screen
        self.setCentralWidget(self.welcome_screen)

        # Connect the signals for navigation
        self.welcome_screen.navigate_to_group_overview.connect(self.show_group_overview)
        self.group_overview_screen.navigate_to_create_bill.connect(self.show_create_bill_screen)

    def show_group_overview(self):
        self.setCentralWidget(self.group_overview_screen)

    def show_create_bill_screen(self):
        self.setCentralWidget(self.create_bill_screen)
