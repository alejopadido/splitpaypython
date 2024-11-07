from PyQt5.QtWidgets import QMainWindow
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.group_overview_screen import GroupOverviewScreen
from ui.screens.create_bill_screen import CreateBillScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay Navigation Example")

        # Initialize the welcome screen and display it
        self.welcome_screen = WelcomeScreen()
        self.setCentralWidget(self.welcome_screen)

        # Connect the signals for navigation
        self.welcome_screen.navigate_to_group_overview.connect(self.show_group_overview)

    def show_group_overview(self):
        self.group_overview_screen = GroupOverviewScreen()  # Create a new instance each time
        self.group_overview_screen.navigate_to_create_bill.connect(self.show_create_bill_screen)
        self.setCentralWidget(self.group_overview_screen)

    def show_create_bill_screen(self):
        self.create_bill_screen = CreateBillScreen()  # Create a new instance each time
        self.create_bill_screen.navigate_back.connect(self.show_group_overview)
        self.setCentralWidget(self.create_bill_screen)
