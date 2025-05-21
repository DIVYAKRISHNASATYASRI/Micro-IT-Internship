import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import hashlib

def generate_key(password: str) -> bytes:
    # Generate a key based on the password using SHA256 hash
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path, password):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()

        key = hashlib.sha256(password.encode()).digest()
        fernet_key = Fernet(base64.urlsafe_b64encode(key))
        encrypted_data = fernet_key.encrypt(data)

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)

        return encrypted_file_path
    except Exception as e:
        return str(e)

def decrypt_file(file_path, password):
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        key = hashlib.sha256(password.encode()).digest()
        fernet_key = Fernet(base64.urlsafe_b64encode(key))
        decrypted_data = fernet_key.decrypt(encrypted_data)

        decrypted_file_path = file_path.replace('.enc', '') + '_decrypted'
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_file_path
    except Exception as e:
        return str(e)

# GUI Setup
import base64

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryption & Decryption Tool")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        # File Selection
        ttk.Label(root, text="File Path:", font=('Arial', 10)).pack(pady=5)
        self.file_entry = ttk.Entry(root, width=60)
        self.file_entry.pack(pady=5)
        ttk.Button(root, text="Browse", command=self.browse_file).pack(pady=5)

        # Password
        ttk.Label(root, text="Password/Key:", font=('Arial', 10)).pack(pady=5)
        self.password_entry = ttk.Entry(root, width=60, show="*")
        self.password_entry.pack(pady=5)

        # Action Buttons
        ttk.Button(root, text="Encrypt File", command=self.encrypt).pack(pady=10)
        ttk.Button(root, text="Decrypt File", command=self.decrypt).pack(pady=5)

        # Status
        self.status_label = ttk.Label(root, text="", foreground='green', font=('Arial', 10))
        self.status_label.pack(pady=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)

    def encrypt(self):
        path = self.file_entry.get()
        password = self.password_entry.get()
        if not path or not password:
            messagebox.showerror("Error", "Please select a file and enter a password.")
            return
        result = encrypt_file(path, password)
        if os.path.isfile(result):
            self.status_label.config(text=f"File encrypted: {result}", foreground="green")
        else:
            self.status_label.config(text=f"Error: {result}", foreground="red")

    def decrypt(self):
        path = self.file_entry.get()
        password = self.password_entry.get()
        if not path or not password:
            messagebox.showerror("Error", "Please select a file and enter a password.")
            return
        result = decrypt_file(path, password)
        if os.path.isfile(result):
            self.status_label.config(text=f"File decrypted: {result}", foreground="green")
        else:
            self.status_label.config(text=f"Error: {result}", foreground="red")


# Run the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
