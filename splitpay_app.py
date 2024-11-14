import tkinter as tk
from tkinter import ttk, messagebox
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
        ttk.Button(frame, text="Member to Member Transaction", command=lambda: self.member_to_member_transaction(username)).pack(pady=10)
        ttk.Button(frame, text="Bill Report by Date and Group", command=self.bill_report_screen).pack(pady=10)
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

        members = db_connection.get_group_member_debts(group_id)

        if members:
            self.clear_window()

            container = ttk.Frame(self.root)
            container.pack(expand=True, fill="both")

            frame = self.create_scrollable_frame(container)

            ttk.Label(frame, text=f"Members of Group ID: {group_id}", font=("Helvetica", 16, "bold")).pack(pady=20)

            columns = ("Name", "Total Debt", "Total Paid", "Payment Status", "Percentage Paid")
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

            ttk.Button(button_frame, text="See Transactions", command=self.see_transactions).pack(pady=5)
            ttk.Button(button_frame, text="Manage Bills", command=self.manage_bills).pack(pady=5)
            ttk.Button(button_frame, text="Add Bill", command=lambda: self.add_bill(username, group_id)).pack(pady=5)
            ttk.Button(button_frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=5)
            ttk.Button(frame, text="Member to Member Transaction", command=lambda: self.member_to_member_transaction(username, group_id)).pack(pady=5)
        else:
            messagebox.showerror("Error", "No financial details available for this group.")

    def member_to_member_transaction(self, username, group_id):
        # Clear the current window to add transaction fields
        self.clear_window()

        # Create a container for the transaction form
        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")
        frame = ttk.Frame(container, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Transaction Form Fields
        ttk.Label(frame, text="Member to Member Transaction", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frame, text="From User ID:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.from_user_entry = ttk.Entry(frame)
        self.from_user_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="To User ID:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.to_user_entry = ttk.Entry(frame)
        self.to_user_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Payment Method (Paypal/Cash):").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.payment_method_entry = ttk.Entry(frame)
        self.payment_method_entry.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Bill ID:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.bill_id_entry = ttk.Entry(frame)
        self.bill_id_entry.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Clear All Debt? (y/n):").grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.clear_all_entry = ttk.Entry(frame)
        self.clear_all_entry.grid(row=6, column=1, pady=5, padx=5)

        # Transaction Button
        ttk.Button(frame, text="Complete Transaction", command=lambda: self.execute_transaction(group_id)).grid(row=7, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.open_group(username, group_id)).grid(row=8, columnspan=2, pady=10)

    def execute_transaction(self, group_id):
        # Get values from the form
        from_user_id = self.from_user_entry.get()
        to_user_id = self.to_user_entry.get()
        amount = float(self.amount_entry.get())
        payment_method = self.payment_method_entry.get().strip().capitalize()
        bill_id = self.bill_id_entry.get()
        clear_all = self.clear_all_entry.get().strip().lower() == 'y'

        # Perform the transaction using db_connection
        transaction_success = db_connection.member_to_member_transaction(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            clear_all=clear_all,
            payment_method=payment_method,
            bill_id=bill_id,
            group_id=group_id
        )

        # Show a success or error message
        if transaction_success:
            messagebox.showinfo("Transaction Completed", f"Transaction from User {from_user_id} to User {to_user_id} completed successfully.")
            self.open_group(self.username, group_id)  # Refresh group view
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

        ttk.Button(frame, text="Add Bill", command=lambda: self.save_bill(username, group_id)).grid(row=8, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.open_group(username, group_id)).grid(row=9, columnspan=2, pady=10)

    def save_bill(self, username, group_id):
        # Collect data from the user
        title = self.title_entry.get()
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        status = self.status_entry.get()
        location = self.location_entry.get()
        bill_type = self.type_entry.get()
        comments = self.comments_entry.get()

        # Add new bill to the database
        bill_id = db_connection.add_bill(title, amount, date, status, location, group_id, bill_type, comments)
        if bill_id:
            messagebox.showinfo("Success", f"Bill added successfully with Bill ID: {bill_id}")
            self.open_group(username, group_id)  # Reopen group to refresh data
        else:
            messagebox.showerror("Error", "Error adding bill. Please try again.")

    # Placeholder methods for not-yet-implemented features
    def manage_group_screen(self, username):
        messagebox.showinfo("Info", "Create / Manage Group functionality not implemented yet.")

    def see_transactions(self):
        messagebox.showinfo("Info", "See transactions functionality not implemented yet.")

    def manage_bills(self):
        report_data = db_connection.get_bill_report()
        
        if report_data:
            self.clear_window()
            
            container = ttk.Frame(self.root)
            container.pack(expand=True, fill="both")

            frame = self.create_scrollable_frame(container)
            
            ttk.Label(frame, text="Bill Report by Date and Group", font=("Helvetica", 16, "bold")).pack(pady=20)
            
            columns = ("Bill Month", "Group 1", "Group 2", "Total")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)

            for row in report_data:
                tree.insert("", tk.END, values=row)
            
            ttk.Button(frame, text="Back", command=lambda: self.main_menu(username)).pack(pady=20)
        else:
            messagebox.showerror("Error", "Failed to generate the bill report.")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SplitPayApp(root)
    root.mainloop()
