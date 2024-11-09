import sys
import db_connection as db_connection

def main():
    # Get user information from the terminal
    username = input("Enter username: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")

    # Check if user exists
    user_exists = db_connection.check_user_exists(username=username, email=email, phone=phone)

    if user_exists:
        print("Login successful! Continuing session...")

        while True:
            print('Options')
            print('''
    0. Exit
    1. Show my groups
    2. Open group
            ''')
            option = input(': ')

            if option == '0':
                print("Exiting session.")
                sys.exit()

            elif option == '1':
                # Show user's groups
                groups = db_connection.get_user_groups(username)
                if groups:
                    print("User is part of the following groups:\n")
                    for group in groups:
                        print(f"Group ID: {group[0]}\n Name: {group[1]}\n Created Date: {group[2]}\n Status: {group[3]}\n")
                else:
                    print("User is not part of any groups.")

            elif option == '2':
                # Placeholder for "Open group" functionality
                group_id = input("Enter the Group ID you want to open: ")
                print(f"Opening details for Group ID: {group_id} (functionality not implemented yet)")

            else:
                print("Invalid option. Please try again.")

    else:
        print("User does not exist. Closing session.")
        sys.exit()

if __name__ == "__main__":
    main()
