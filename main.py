import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import config.db_connection as db_connection 

def main():
    # Test login
    username = 'Alejandro'
    email = 'alejo@email.com'   
    phone = '3186064342'

    user_exists = db_connection.check_user_exists(username=username, email=email, phone=phone)
    print('User exists: ', user_exists) 
    
    # Test group overview
    
if __name__ == "__main__":
    main()
