import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(700, 400)  # Set window size
    window.show()            # Display the window
    sys.exit(app.exec_())    # Run the app

if __name__ == "__main__":
    main()
