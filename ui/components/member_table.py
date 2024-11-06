from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class MemberTable(QTableWidget):
    def __init__(self):
        super().__init__(4, 2)  # For now, 4 rows and 2 columns
        self.setHorizontalHeaderLabels(["Members", "Debt"])
        self.setStyleSheet("background-color: #f0f0ff; border-radius: 10px;")

        # Add demo data
        members = ["Gladis Osorio", "Gloria Eugenia", "Elkin Mosquera", "Antonio Vivaldi"]
        debts = [-20.0, 75.0, -20.0, 1275.0]

        for row, (member, debt) in enumerate(zip(members, debts)):
            self.setItem(row, 0, QTableWidgetItem(member))
            debt_item = QTableWidgetItem(f"${debt:,.2f}")
            debt_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if debt < 0:
                debt_item.setForeground(QColor("red"))
            else:
                debt_item.setForeground(QColor("green"))
            self.setItem(row, 1, debt_item)

        self.resizeColumnsToContents()
        self.setMaximumHeight(150)
