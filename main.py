import customtkinter as ctk
import sqlite3
from tkinter import ttk, messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

conn = sqlite3.connect("Accounts & Passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT,
    username TEXT,
    password TEXT,
    gmail TEXT
   
)
""")
conn.commit()

def accounts_password():
    site = account_site_var.get()
    try:
        username = account_username_var.get()
        password = account_password_var.get()
    except ValueError:
        messagebox.showerror("Error", "Enter the Account and the password.")
        return
    gmail = gmail_account_used_var.get()

    if site and len(username) > 0 and len(password) > 0:
        cursor.execute("SELECT id FROM accounts WHERE site = ?",(site,))
        existing_account = cursor.fetchone()
        if existing_account:
            cursor.execute("UPDATE accounts SET username = ?, password = ?, gmail = ?, WHERE id = ?",
                           (username, password, existing_account[0]))
        else:
            cursor.execute("INSERT INTO accounts (site, username, password, gmail) VALUES (?, ?, ?, ?)",
                           (site, username, password, gmail))
        conn.commit()
        account_site_var.set("")
        account_username_var.set("")
        account_password_var.set("")
        gmail_account_used_var.set("")
        update_accounts_view()
        messagebox.showinfo("Success","Account added/updated successfully.")
    else:
        messagebox.showerror("Error","All fields are required.")

def show_account_details(event):
    selected_account = account_tree.selection()
    if selected_account:
        account = account_tree.account(selected_account[0])['values']
        messagebox.showinfo("Account Details",f"Account Details:\n{account}")
def update_accounts_view():
    for row in account_tree.get_children():
        account_tree.delete(row)
    cursor.execute("SELECT id, site, username, password, gmail FROM accounts")
    for row in cursor.fetchall():
        account_tree.insert("","end", values=row)

def strength_check():
    password = password_strength_checker_entry.get()
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char in "!@#$%^&*()<>?|:{}" for char in password):
        strength += 1
    password_strength_checker_result_label.configure(text=f"Strength is {strength}/4")

root = ctk.CTk()
root.title("Password Strength Checker & Accounts Manager")
root.geometry('950x450')

nav_frame = ctk.CTkFrame(root, width=200)
nav_frame.pack(side="left", fill="y")

content_frame = ctk.CTkFrame(root)
content_frame.pack(side="right", fill="both", expand=True)

def show_frame(frame):
    frame.tkraise()

password_strength_checker_frame = ctk.CTkFrame(content_frame)
accounts_password_frame = ctk.CTkFrame(content_frame)

for frame in (password_strength_checker_frame,accounts_password_frame):
    frame.grid(row=0, column=0, sticky="nsew")

content_frame.grid_columnconfigure(0,weight=1)
content_frame.grid_rowconfigure(0,weight=1)

ctk.CTkLabel(password_strength_checker_frame, text="Password Strength Checker", font=("Arial", 24, "bold")).pack(pady=20)
password_strength_checker_label = ctk.CTkLabel(password_strength_checker_frame, text="Enter the password: ")
password_strength_checker_label.pack(pady=20)
password_strength_checker_entry = ctk.CTkEntry(password_strength_checker_frame, show="*")
password_strength_checker_entry.pack(pady=10)
password_strength_checker_check_button = ctk.CTkButton(password_strength_checker_frame, text="Check Strength", command=strength_check)
password_strength_checker_check_button.pack(pady=20)
password_strength_checker_result_label = ctk.CTkLabel(password_strength_checker_frame, text="")
password_strength_checker_result_label.pack(pady=20)

ctk.CTkLabel(accounts_password_frame, text="Manage Accounts and Passwords", font=("Arial", 24, "bold")).pack(pady=20)
account_site_var = ctk.StringVar()
account_username_var = ctk.StringVar()
account_password_var = ctk.StringVar()
gmail_account_used_var = ctk.StringVar()

account_row_frame = ctk.CTkFrame(accounts_password_frame)
account_row_frame.pack(fill="x", padx=20, pady=5)

ctk.CTkLabel(account_row_frame, text="Website: ").pack(side="left", padx=5)
ctk.CTkEntry(account_row_frame, textvariable=account_site_var).pack(side="left", padx=5)

ctk.CTkLabel(account_row_frame, text="Username: ").pack(side="left", padx=5)
ctk.CTkEntry(account_row_frame, textvariable=account_username_var).pack(side="left", padx=5)

ctk.CTkLabel(account_row_frame, text="Password: ").pack(side="left", padx=5)
ctk.CTkEntry(account_row_frame, textvariable=account_password_var).pack(side="left", padx=5)

ctk.CTkLabel(accounts_password_frame, text="Gmail: ").pack(fill="x", pady=5, padx=10)
ctk.CTkEntry(accounts_password_frame, textvariable=gmail_account_used_var).pack(fill="x", pady=5, padx=10)

ctk.CTkButton(accounts_password_frame, text="Add/Update Account", command=accounts_password).pack(pady=10)

account_tree = ttk.Treeview(accounts_password_frame, columns=("ID", "Website", "Account Username", "Account Password", "Account Gmail"), show="headings")
account_tree.pack(pady=10, fill="both", expand=True)
for col in ("ID", "Website", "Account Username", "Account Password", "Account Gmail"):
    account_tree.heading(col,text=col)
account_tree.bind("<ButtonRelease-1>", lambda event: show_account_details(event))

ctk.CTkButton(nav_frame, text="Password Strength Checker", command=lambda: show_frame(password_strength_checker_frame)).pack(pady=10)
ctk.CTkButton(nav_frame, text="Accounts and Password", command=lambda: show_frame(accounts_password_frame)).pack(pady=10)

show_frame(password_strength_checker_frame)

update_accounts_view()

root.mainloop()
