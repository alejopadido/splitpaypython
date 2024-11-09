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
                # Open group functionality
                group_id = input("Enter the Group ID you want to open: ")

                # Get and display group members before showing other options
                members = db_connection.get_group_members(group_id)
                if members:
                    print(f"Members of Group ID: {group_id}\n")
                    for member in members:
                        print(f"User ID: {member[0]}, Name: {member[1]}, Email: {member[2]}\n")
                else:
                    print("No members found in this group.\n")

                # Secondary options menu for group actions
                while True:
                    print(f"Options for Group ID: {group_id}")
                    print('''
        0. Back
        1. See transactions
        2. Manage bills
        3. Add bill
                    ''')
                    group_option = input(': ')

                    if group_option == '0':
                        # Go back to the main menu
                        break

                    elif group_option == '1':
                        # Placeholder for "See transactions"
                        print(f"Displaying transactions for Group ID: {group_id} (functionality not implemented yet)")

                    elif group_option == '2':
                        # Placeholder for "Manage bills"
                        print(f"Managing bills for Group ID: {group_id} (functionality not implemented yet)")

                    elif group_option == '3':
                        # Placeholder for "Add bill"
                        print(f"Adding a bill for Group ID: {group_id} (functionality not implemented yet)")

                    else:
                        print("Invalid option. Please try again.")

            else:
                print("Invalid option. Please try again.")

    else:
        print("User does not exist. Closing session.")
        sys.exit()

if __name__ == "__main__":
    main()
