from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class ActionButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Transactions button
        transactions_button = QPushButton("Transactions")
        transactions_button.setStyleSheet("background-color: #3D5AFE; color: white; font-weight: bold; padding: 8px;")
        transactions_button.setFixedWidth(120)
        layout.addWidget(transactions_button)

        # Manage button
        manage_button = QPushButton("Manage")
        manage_button.setStyleSheet("background-color: #3D5AFE; color: white; font-weight: bold; padding: 8px;")
        manage_button.setFixedWidth(120)
        layout.addWidget(manage_button)

        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
