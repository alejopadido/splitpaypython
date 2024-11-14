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

    def member_to_member_transaction(self, username):
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

        ttk.Button(frame, text="Submit", command=self.process_member_to_member_transaction).grid(row=8, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(username)).grid(row=9, columnspan=2, pady=10)

    def process_member_to_member_transaction(self):
        from_user_id = self.from_user_id_entry.get()
        to_user_id = self.to_user_id_entry.get()
        amount = float(self.amount_entry.get())
        bill_id = self.bill_id_entry.get()
        clear_all = self.clear_all_var.get()
        payment_method = self.payment_method_entry.get().strip().capitalize()

        group_id_input = self.group_id_entry_transaction.get()
        group_id = int(group_id_input) if group_id_input else None

        transaction_success = db_connection.member_to_member_transaction(
            from_user_id, to_user_id, amount, clear_all, payment_method, bill_id, group_id
        )
        if transaction_success:
            messagebox.showinfo("Success", "Transaction completed successfully!")
        else:
            messagebox.showerror("Error", "Transaction failed. Please check the details and try again.")

    def bill_report_screen(self):
        self.clear_window()

        container = ttk.Frame(self.root)
        container.pack(expand=True, fill="both")

        frame = self.create_scrollable_frame(container)

        ttk.Label(frame, text="Bill Report by Date and Group", font=("Helvetica", 16, "bold")).pack(pady=20)

        report_data = db_connection.get_bill_report()

        if report_data:
            columns = ("Group ID", "Bill ID", "Title", "Amount", "Date", "Status", "Location", "Comments")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.pack(expand=True, fill="both")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)

            for data in report_data:
                tree.insert("", tk.END, values=data)

            tree.tag_configure('oddrow', background='#E8E8E8')
            tree.tag_configure('evenrow', background='#DFDFDF')

        else:
            ttk.Label(frame, text="No bill report available.").pack(pady=5)

        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=20)

    # Placeholder methods for not-yet-implemented features
    def manage_group_screen(self, username):
        messagebox.showinfo("Info", "Create / Manage Group functionality not implemented yet.")

    def see_transactions(self):
        messagebox.showinfo("Info", "See transactions functionality not implemented yet.")

    def manage_bills(self):
        messagebox.showinfo("Info", "Manage bills functionality not implemented yet.")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SplitPayApp(root)
    root.mainloop()
