from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt

class MemberCheckboxList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Sample members for the demo
        members = ["Gladis Osorio", "Gloria Eugenia", "Elkin Mosquera", "Antonio Vivaldi"]

        # Add a checkbox for each member
        self.checkboxes = []
        for member in members:
            h_layout = QHBoxLayout()
            label = QLabel(member)
            label.setStyleSheet("font-size: 14px; color: black;")
            checkbox = QCheckBox()
            h_layout.addWidget(label)
            h_layout.addWidget(checkbox)
            h_layout.setAlignment(Qt.AlignLeft)
            layout.addLayout(h_layout)
            self.checkboxes.append(checkbox)

    def get_selected_members(self):
        return [checkbox.isChecked() for checkbox in self.checkboxes]
