from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from ui.components.title_label import TitleLabel
from ui.components.subtitle_label import SubtitleLabel
from ui.components.input_field import InputField
from ui.components.done_button import DoneButton

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay")

        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title and subtitle
        title = TitleLabel("Welcome to SplitPay!")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = SubtitleLabel("Enter your information and you'll be ready to go")
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Input fields
        self.username_field = InputField("Username")
        layout.addWidget(self.username_field, alignment=Qt.AlignCenter)

        self.email_field = InputField("Email")
        layout.addWidget(self.email_field, alignment=Qt.AlignCenter)

        self.phone_field = InputField("Phone")
        layout.addWidget(self.phone_field, alignment=Qt.AlignCenter)
        
        layout.addSpacing(20)

        # Done button
        done_button = DoneButton("Done", self.on_done)
        layout.addWidget(done_button, alignment=Qt.AlignCenter)

    def on_done(self):
        # Placeholder for what to do when "Done" is clicked
        print("User Info Submitted:", self.username_field.text(), self.email_field.text(), self.phone_field.text())
