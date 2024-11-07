from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton
from ui.components.title_label import TitleLabel
from ui.components.input_field import InputField
from ui.components.member_checkbox_list import MemberCheckboxList
from ui.components.filled_button import FilledButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class CreateBillScreen(QWidget):
    # Define a custom signal to navigate back to the group overview screen
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Set up the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Back Button (Arrow Button)
        back_button = QToolButton()
        back_button.setIcon(QIcon("assets/icons/arrow_back.png")) 
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("background: transparent; border: none;")
        back_button.clicked.connect(self.on_back)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Title Label
        title = TitleLabel("Create a new Bill")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Container for the form content with a background color
        form_container = QWidget()
        form_container.setStyleSheet("background-color: #f0f0ff; border-radius: 15px;")
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_container.setLayout(form_layout)

        # Amount Input Field with Dollar Symbol
        amount_layout = QHBoxLayout()
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(5)  # Reduce spacing between label and text field

        amount_label = QLabel("$")
        amount_label.setStyleSheet("font-size: 18px; color: #3D5AFE; font-weight: bold;")
        amount_label.setFixedWidth(15)  # Set a fixed width for the label to align it better with the text field

        self.amount_field = InputField("Amount")
        self.amount_field.setFixedWidth(150)  # Set a fixed width for consistent alignment

        amount_layout.addWidget(amount_label, alignment=Qt.AlignCenter)
        amount_layout.addWidget(self.amount_field, alignment=Qt.AlignCenter)
        form_layout.addLayout(amount_layout)

        # Member Checkbox List
        member_list = MemberCheckboxList()
        form_layout.addWidget(member_list, alignment=Qt.AlignCenter)

        # Add form container to the main layout
        layout.addWidget(form_container, alignment=Qt.AlignCenter)

        # Confirm Button
        confirm_button = FilledButton("Confirm", self.on_confirm)
        layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

    def on_back(self):
        # Emit the custom signal to navigate back
        self.navigate_back.emit()

    def on_confirm(self):
        # Placeholder action when "Confirm" is clicked
        print("Bill Confirmed!")
