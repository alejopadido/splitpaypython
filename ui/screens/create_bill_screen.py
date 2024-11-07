from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from ui.components.title_label import TitleLabel
from ui.components.input_field import InputField
from ui.components.member_checkbox_list import MemberCheckboxList
from ui.components.filled_button import FilledButton
from PyQt5.QtCore import Qt

class CreateBillScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title Label
        title = TitleLabel("Create a new Bill")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Amount Input Field
        amount_layout = QHBoxLayout()
        amount_label = QLabel("$")
        amount_label.setStyleSheet("font-size: 18px; color: #3D5AFE; font-weight: bold;")
        self.amount_field = InputField("Amount")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_field)
        amount_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(amount_layout)

        # Member Checkbox List
        member_list = MemberCheckboxList()
        layout.addWidget(member_list, alignment=Qt.AlignCenter)

        # Confirm Button
        confirm_button = FilledButton("Confirm", self.on_confirm)
        layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

    def on_confirm(self):
        # Placeholder action when "Confirm" is clicked
        print("Bill Confirmed!")
