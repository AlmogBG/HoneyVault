import tkinter as tk
from tkinter import filedialog, messagebox
from vault_context import VaultContext

class VaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure HoneyVault")
        self.root.geometry("400x250")
        self.vault = VaultContext()
        
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="Status: Select a folder", font=("Arial", 12))
        self.status_label.pack(pady=20)

        self.btn_select = tk.Button(self.root, text="Select Folder", command=self.select_folder, width=20)
        self.btn_select.pack(pady=5)

        self.btn_lock = tk.Button(self.root, text="LOCK VAULT", bg="red", fg="white", command=self.perform_lock, width=20)
        self.btn_lock.pack(pady=5)

        self.btn_unlock = tk.Button(self.root, text="UNLOCK VAULT", bg="green", fg="white", command=self.perform_unlock, width=20)
        self.btn_unlock.pack(pady=5)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.vault.set_vault_path(path)
            self.vault.start_protection()
            self.status_label.config(text=f"Selected: {path}")
            messagebox.showinfo("Ready", "Folder selected & Honey Traps deployed!")

    def perform_lock(self):
        if not self.vault.root_folder:
            messagebox.showwarning("Error", "Please select a folder first!")
            return
        
        self.vault.lock_vault()
        self.status_label.config(text="Status: LOCKED (Secured)", fg="red")
        messagebox.showinfo("Success", "Vault Locked & Key Saved!")

    def perform_unlock(self):
        if not self.vault.root_folder:
            messagebox.showwarning("Error", "Please select a folder first!")
            return
            
        self.vault.unlock_vault()
        self.status_label.config(text="Status: UNLOCKED (Access Granted)", fg="green")
        messagebox.showinfo("Success", "Vault Unlocked & Key Destroyed!")

if __name__ == "__main__":
    import os  
    
    root = tk.Tk()
    app = VaultApp(root)
    
    def on_close():
        root.title("Cleaning up... Please wait...")
        if hasattr(app, 'vault'):
            app.vault.stop_services()
        
        root.destroy()
        os._exit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()