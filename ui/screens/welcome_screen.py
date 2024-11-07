from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from ui.components.title_label import TitleLabel
from ui.components.subtitle_label import SubtitleLabel
from ui.components.input_field import InputField
from ui.components.filled_button import FilledButton
import db_connection  # Import the database connection module

class WelcomeScreen(QWidget):
    # Define a custom signal for requesting navigation
    navigate_to_group_overview = pyqtSignal()

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
        done_button = FilledButton("Done", self.on_done)
        layout.addWidget(done_button, alignment=Qt.AlignCenter)

        # Error Label for incorrect user information
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

    def on_done(self):
        # Get input values
        username = self.username_field.text()
        email = self.email_field.text()
        phone = self.phone_field.text()

        # Check user information in the database using the `db_connection` module
        if db_connection.check_user_exists(username, email, phone):
            # User exists, navigate to group overview
            self.navigate_to_group_overview.emit()
        else:
            # User does not exist, show error message
            self.error_label.setText("Incorrect user information. Please try again.")
