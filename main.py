from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import sys

from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplitPay")

        # Set up layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title and subtitle
        title = QLabel("Welcome to SplitPay!")
        title.setStyleSheet("font-size: 24px; color: #3D5AFE; font-weight: bold;")
        layout.addWidget(title, alignment= Qt.AlignCenter)

        subtitle = QLabel("Enter your information and you'll be ready to go")
        subtitle.setStyleSheet("color: gray; font-size: 14px;")
        layout.addWidget(subtitle, alignment= Qt.AlignCenter)

        # Input fields
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        layout.addWidget(self.username_field, alignment = Qt.AlignCenter)

        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        layout.addWidget(self.email_field, alignment = Qt.AlignCenter)

        self.phone_field = QLineEdit()
        self.phone_field.setPlaceholderText("Phone")
        layout.addWidget(self.phone_field, alignment = Qt.AlignCenter)
        
        layout.addSpacing(20)

        # Done button
        done_button = QPushButton("Done")
        done_button.setStyleSheet("background-color: #3D5AFE; color: white; font-weight: bold; padding: 8px;")
        done_button.clicked.connect(self.on_done)
        layout.addWidget(done_button, alignment = Qt.AlignCenter)

    def on_done(self):
        # Placeholder for what to do when "Done" is clicked
        print("User Info Submitted:", self.username_field.text(), self.email_field.text(), self.phone_field.text())

# Set up the application
app = QApplication(sys.argv)
window = MainWindow()
window.resize(700, 400)  # Set window size  
window.show()            # Display the window
sys.exit(app.exec_())    # Run the app
