import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import db_connection

class SplitPayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SplitPayApp - Group Management System")
        self.root.geometry("900x506")  # Set default window size with a 16:9 aspect ratio
        self.root.minsize(800, 450)  # Set a minimum size with a reasonable 16:9 aspect ratio

        # Configure a modern style for the application
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10, foreground="black")  # Set button text to black
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#F0F0F0")
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Treeview", borderwidth=1, relief="solid")
        self.style.configure("Treeview.Heading", background="#f0f0f0", relief="flat")

        # Initialize with the login screen
        self.login_screen()

    def clear_window(self):
        """Utility to clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame for larger content."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def login_screen(self):
        self.clear_window()

        # Create a frame to hold the login widgets and center it
        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")
        frame = ttk.Frame(container, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login fields
        ttk.Label(frame, text="Enter Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Enter Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Enter Phone Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.grid(row=2, column=1, pady=5)

        # Login button
        ttk.Button(frame, text="Login", command=self.login).grid(row=3, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        user_exists = db_connection.check_user_exists(username=username, email=email, phone=phone)

        if user_exists:
            messagebox.showinfo("Login Successful", "Continuing session...")
            self.main_menu(username)
        else:
            messagebox.showerror("Error", "User does not exist. Closing session.")
            self.root.quit()

    def main_menu(self, username):
        self.clear_window()

        # Main Menu
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Main Menu", font=("Helvetica", 16, "bold")).pack(pady=20)

        ttk.Button(frame, text="Show My Groups", command=lambda: self.show_groups(username)).pack(pady=10)
        ttk.Button(frame, text="Open Group", command=lambda: self.open_group_screen(username)).pack(pady=10)
        ttk.Button(frame, text="Create / Manage Group", command=lambda: self.manage_group_screen(username)).pack(pady=10)
        ttk.Button(frame, text="Manage Bills", command=lambda: self.manage_bills(username)).pack(pady=5)
        #ttk.Button(frame, text="Member to Member Transaction", command=lambda: self.member_to_member_transaction(username)).pack(pady=10)
        # ttk.Button(frame, text="Bill Report by Date and Group", command=self.bill_report_screen).pack(pady=10)
        ttk.Button(frame, text="Exit", command=self.root.quit).pack(pady=10)

    def show_groups(self, username):
        self.clear_window()

        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        frame = self.create_scrollable_frame(container)

        ttk.Label(frame, text="My Groups", font=("Helvetica", 16, "bold")).pack(pady=20)

        groups = db_connection.get_user_groups(username)

        if groups:
            columns = ("Group ID", "Name", "Created Date", "Status")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)

            for group in groups:
                tree.insert("", tk.END, values=group)

            tree.tag_configure('oddrow', background='#E8E8E8')
            tree.tag_configure('evenrow', background='#DFDFDF')

        else:
            ttk.Label(frame, text="User is not part of any groups.").pack(pady=5)

        ttk.Button(frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=20)

    def open_group_screen(self, username):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Enter Group ID to open:", font=("Helvetica", 14)).pack(pady=10)
        self.group_id_entry = ttk.Entry(frame)
        self.group_id_entry.pack(pady=10)

        ttk.Button(frame, text="Open Group", command=lambda: self.open_group(username)).pack(pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=10)

    def open_group(self, username, group_id=None):
        if not group_id:
            group_id = self.group_id_entry.get()

        # First, try to get group member debts
        members = db_connection.get_group_member_debts(group_id)

        # If no members with debt are found, fall back to just getting the group members
        if not members:
            members = db_connection.get_group_members(group_id)

        # If we still have no members, show an error
        if not members:
            messagebox.showerror("Error", "No members available for this group.")
            return

        # Otherwise, proceed with showing group members
        self.clear_window()

        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        frame = self.create_scrollable_frame(container)

        ttk.Label(frame, text=f"Members of Group ID: {group_id}", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Adjust columns based on what data we have
        columns = ("Name", "Total Debt", "Total Paid", "Payment Status", "Percentage Paid") if db_connection.get_group_member_debts(group_id) else ("User ID", "Name", "Email")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.pack(expand=True, fill="both")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.W)

        for index, member in enumerate(members):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            tree.insert("", tk.END, values=member, tags=(tag,))

        tree.tag_configure('oddrow', background='#E8E8E8')
        tree.tag_configure('evenrow', background='#DFDFDF')

        # Add buttons for actions after the Treeview to ensure visibility
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="See Transactions", command=lambda: self.see_transactions(username, group_id)).pack(pady=5)
        ttk.Button(button_frame, text="Add Bill", command=lambda: self.add_bill(username, group_id)).pack(pady=5)
        ttk.Button(button_frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=5)
        ttk.Button(button_frame, text="Member to Member Transaction", command=lambda: self.member_to_member_transaction(username, group_id)).pack(pady=5)


    def see_transactions(self, username, group_id):
        self.clear_window()

        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        frame = self.create_scrollable_frame(container)

        ttk.Label(frame, text=f"Transactions for Group ID: {group_id}", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Get transactions from the database
        transactions = db_connection.get_group_transactions(group_id)

        if transactions:
            columns = ("Transaction ID", "Amount", "Date", "Description", "Payer ID", "Payee ID", "Status", "Bill ID")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)

            for index, transaction in enumerate(transactions):
                tag = 'oddrow' if index % 2 == 0 else 'evenrow'
                tree.insert("", tk.END, values=transaction, tags=(tag,))

            tree.tag_configure('oddrow', background='#E8E8E8')
            tree.tag_configure('evenrow', background='#DFDFDF')

        else:
            ttk.Label(frame, text="No transactions found for this group.").pack(pady=5)

        ttk.Button(frame, text="Back", command=lambda: self.open_group(username=username, group_id=group_id)).pack(pady=20)



    def member_to_member_transaction(self, username, group_id):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Member to Member Transaction", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Input fields for the transaction
        ttk.Label(frame, text="Payer User ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.from_user_id_entry = ttk.Entry(frame)
        self.from_user_id_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Payee User ID:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.to_user_id_entry = ttk.Entry(frame)
        self.to_user_id_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Bill ID:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.bill_id_entry = ttk.Entry(frame)
        self.bill_id_entry.grid(row=4, column=1, pady=5)

        self.clear_all_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Clear All Debt", variable=self.clear_all_var).grid(row=5, column=1, sticky=tk.W, pady=5)

        ttk.Label(frame, text="Payment Method (Paypal/Cash):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.payment_method_entry = ttk.Entry(frame)
        self.payment_method_entry.grid(row=6, column=1, pady=5)

        ttk.Label(frame, text="Group ID (optional):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.group_id_entry_transaction = ttk.Entry(frame)
        self.group_id_entry_transaction.grid(row=7, column=1, pady=5)

        ttk.Button(frame, text="Submit", command=lambda: self.execute_transaction(group_id)).grid(row=8, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.open_group(username, group_id)).grid(row=9, columnspan=2, pady=10)

    def execute_transaction(self, group_id):
        # Get values from the form
        from_user_id = self.from_user_id_entry.get()
        to_user_id = self.to_user_id_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        bill_id = self.bill_id_entry.get()
        clear_all = self.clear_all_var.get()  # This will be True or False based on the checkbox
        payment_method = self.payment_method_entry.get().strip().capitalize()
        group_id_optional = self.group_id_entry_transaction.get().strip()
        group_id_final = group_id if not group_id_optional else int(group_id_optional)

        # Check if required fields are filled
        if not from_user_id or not to_user_id or not payment_method:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Perform the transaction using db_connection
        transaction_success = db_connection.member_to_member_transaction(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            clear_debt=clear_all,
            payment_method=payment_method,
            billId=bill_id,
            group_id=group_id_final
        )

        # Show a success or error message
        if transaction_success:
            messagebox.showinfo("Transaction Completed", f"Transaction from User ID {from_user_id} to User ID {to_user_id} completed successfully.")
            self.open_group(self.username, group_id_final)  # Refresh group view
        else:
            messagebox.showerror("Transaction Failed", "Failed to complete the transaction. Please check the details and try again.")
   

    def add_bill(self, username, group_id):
        self.clear_window()

        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        frame = ttk.Frame(container, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Add New Bill", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Bill details form arranged in two columns
        ttk.Label(frame, text="Title:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.title_entry = ttk.Entry(frame)
        self.title_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Amount:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Status (Pending/Approved/Debt/Paid):").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.status_entry = ttk.Entry(frame)
        self.status_entry.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Location (optional):").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.location_entry = ttk.Entry(frame)
        self.location_entry.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Type (e.g., Lodging, Food, Office):").grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Comments (optional):").grid(row=7, column=0, sticky=tk.W, pady=5, padx=5)
        self.comments_entry = ttk.Entry(frame)
        self.comments_entry.grid(row=7, column=1, pady=5, padx=5)

        # Button to upload receipt image
        self.image_path = None  # Store the path of the selected image
        ttk.Button(frame, text="Upload Receipt Image", command=self.upload_image).grid(row=8, columnspan=2, pady=10)

        ttk.Button(frame, text="Add Bill", command=lambda: self.save_bill(username, group_id)).grid(row=9, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.open_group(username, group_id)).grid(row=10, columnspan=2, pady=10)

    def upload_image(self):
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Selected image: {os.path.basename(file_path)}")

    def save_bill(self, username, group_id):
        # Collect data from the user
        title = self.title_entry.get()
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        status = self.status_entry.get()
        location = self.location_entry.get()
        bill_type = self.type_entry.get()
        comments = self.comments_entry.get()

        # Read the selected image file, if any
        image_data = None
        if self.image_path:
            with open(self.image_path, 'rb') as file:
                image_data = file.read()

        # Add new bill to the database
        bill_id = db_connection.add_bill(title, amount, date, status, location, group_id, bill_type, comments, image_data)
        if bill_id:
            messagebox.showinfo("Success", f"Bill added successfully with Bill ID: {bill_id}")  
            self.open_group(username, group_id)  # Reopen group to refresh data
        else:
            messagebox.showerror("Error", "Error adding bill. Please try again.")

    def manage_group_screen(self, username):
        self.clear_window()

        # Main container frame for all elements
        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        # Top frame for group details
        top_frame = ttk.Frame(container, padding="20")
        top_frame.pack(side="top", fill="x")

        ttk.Label(top_frame, text="Manage Group", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Input for group name
        ttk.Label(top_frame, text="Enter Group Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.group_name_entry = ttk.Entry(top_frame, width=30)
        self.group_name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Dropdown for group leader selection
        ttk.Label(top_frame, text="Select Group Leader:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Get all users from the database
        users = db_connection.get_all_users()

        # Mapping of display text to user IDs, using both name and email to avoid duplicates
        self.user_display_mapping = {f"{user[1]} ({user[2]})": user[0] for user in users}  # Mapping name (with email) to user ID
        leader_display_names = list(self.user_display_mapping.keys())

        # Debugging step to print out the leader names and mapping
        print("Leader Display Mapping:", self.user_display_mapping)

        self.leader_combobox = ttk.Combobox(top_frame, values=leader_display_names, width=28)
        self.leader_combobox.grid(row=2, column=1, pady=5, padx=5)

        # Frame for members selection
        member_frame = self.create_scrollable_frame(container)
        ttk.Label(member_frame, text="Select Members", font=("Helvetica", 14)).pack(pady=10)

        # A dictionary to hold member checkboxes
        self.member_checkboxes = {}

        # Creating checkboxes for each user
        for index, user in enumerate(users):
            user_id, name, email = user  # Extracting data from tuple
            member_var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(member_frame, text=f"{name} ({email})", variable=member_var)
            checkbox.pack(anchor=tk.W, pady=2)
            self.member_checkboxes[user_id] = member_var

        # Bottom frame for action buttons
        button_frame = ttk.Frame(container, padding="20")
        button_frame.pack(side="bottom", fill="x")

        ttk.Button(button_frame, text="Done", command=lambda: self.create_or_manage_group(username)).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(button_frame, text="Back", command=lambda: self.main_menu(username)).grid(row=0, column=3, padx=10, pady=10)

    def create_or_manage_group(self, username):
        # Retrieve the group name from the entry widget
        group_name = self.group_name_entry.get().strip()  # Use strip to remove extra spaces
        leader_display_name = self.leader_combobox.get().strip()

        # Add debugging to see what's being retrieved
        print(f"Group Name: '{group_name}'")
        print(f"Leader Display Name: '{leader_display_name}'")

        # Check if the group name and leader name are provided
        if not group_name:
            messagebox.showerror("Error", "Please enter a group name.")
            return
        if not leader_display_name:
            messagebox.showerror("Error", "Please select a group leader.")
            return

        # Find the user ID of the selected leader by their name and email combination
        leader_id = self.user_display_mapping.get(leader_display_name)

        # Debugging step to ensure leader ID was found
        print(f"Leader ID found: {leader_id}")

        if leader_id is None:
            messagebox.showerror("Error", "Selected leader could not be found. Please try again.")
            return

        # Get the list of selected members
        selected_members = [user_id for user_id, var in self.member_checkboxes.items() if var.get()]

        # Check if there are selected members
        if not selected_members:
            messagebox.showerror("Error", "Please select at least one member for the group.")
            return

        # Create the group with members and the leader
        group_id = db_connection.create_group_with_members(group_name, username, selected_members, leader_id)

        if group_id:
            messagebox.showinfo("Success", f"Group '{group_name}' created successfully.")
            self.main_menu(username)
        else:
            messagebox.showerror("Error", "Failed to create the group. Please try again.")


    def manage_bills(self, username):
        report_data, totals = db_connection.get_bill_report()
        
        if report_data:
            self.clear_window()
            
            container = ttk.Frame(self.root)
            container.pack(expand=True, fill="both")

            frame = self.create_scrollable_frame(container)
            
            ttk.Label(frame, text="Bill Report by Date and Group", font=("Helvetica", 16, "bold")).pack(pady=20)
            
            # Get unique group names for column headers
            group_names = set()
            for groups in report_data.values():
                group_names.update(groups.keys())
            group_names = sorted(group_names)

            # Set up Treeview columns
            columns = ["Bill Month"] + group_names + ["Total"]
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)

            # Insert data rows
            for bill_month, groups in report_data.items():
                row = [bill_month]
                total = 0
                for group in group_names:
                    amount = groups.get(group, 0)
                    row.append(amount)
                    total += amount
                row.append(total)
                tree.insert("", tk.END, values=row)

            # Insert total row
            total_row = ["Total"]
            for group in group_names:
                total_row.append(totals.get(group, 0))
            total_row.append(totals.get("Total", 0))
            tree.insert("", tk.END, values=total_row)

            ttk.Button(frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=20)
        else:
            messagebox.showerror("Error", "Failed to generate the bill report.")



# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SplitPayApp(root)
    root.mainloop()
