from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.components.title_label import TitleLabel
from ui.components.member_table import MemberTable
from ui.components.action_buttons import ActionButtons
from ui.components.filled_button import FilledButton
from PyQt5.QtCore import Qt, pyqtSignal

class GroupOverviewScreen(QWidget):
    # Define a custom signal for requesting navigation to the create bill screen
    navigate_to_create_bill = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title Label
        title = TitleLabel("Hello Kitty Army")
        layout.addWidget(title)

        # Member Table
        member_table = MemberTable()
        layout.addWidget(member_table, alignment=Qt.AlignCenter)

        # Action Buttons (Transactions & Manage)
        action_buttons = ActionButtons()
        layout.addWidget(action_buttons, alignment=Qt.AlignCenter)

        # Create Bill Button - Properly pass the callback function
        create_bill_button = FilledButton('Create Bill', self.on_create_bill)
        layout.addWidget(create_bill_button, alignment=Qt.AlignCenter)

    # Emit the signal to navigate to the create bill screen
    def on_create_bill(self):
        self.navigate_to_create_bill.emit()
