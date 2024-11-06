from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.components.title_label import TitleLabel
from ui.components.member_table import MemberTable
from ui.components.action_buttons import ActionButtons
from ui.components.filled_button import FilledButton
from PyQt5.QtCore import Qt

class GroupOverviewScreen(QWidget):
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

    # Define the callback function to be called when the button is clicked
    def on_create_bill(self):
        print('Create Bill Button Pressed!')
