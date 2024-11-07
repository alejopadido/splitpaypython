from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt

class MemberCheckboxList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Sample members for the demo
        members = ["Gladis Osorio", "Gloria Eugenia", "Elkin Mosquera", "Antonio Vivaldi"]

        # Add a checkbox for each member with a consistent layout
        self.checkboxes = []
        for member in members:
            h_layout = QHBoxLayout()
            h_layout.setContentsMargins(0, 5, 0, 5)  # Add some padding for spacing
            h_layout.setSpacing(10)  # Add spacing between label and checkbox

            # Member Label
            label = QLabel(member)
            label.setStyleSheet("font-size: 14px; color: black;")
            label.setFixedWidth(150)  # Set fixed width to align all labels

            # Member Checkbox
            checkbox = QCheckBox()

            # Add label and checkbox to the horizontal layout
            h_layout.addWidget(label, alignment=Qt.AlignLeft)
            h_layout.addWidget(checkbox, alignment=Qt.AlignRight)

            # Add horizontal layout to the main vertical layout
            layout.addLayout(h_layout)
            self.checkboxes.append(checkbox)

    def get_selected_members(self):
        return [checkbox.isChecked() for checkbox in self.checkboxes]
