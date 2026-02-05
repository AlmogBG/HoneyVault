import os
from cryptography.fernet import Fernet
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
class CryptoService:
    """
    Service responsible for the low-level encryption and decryption of files.
    It is stateless: it receives a key for each operation and does not store it.
    """

    
    IGNORE_FILES = [
        "main_gui.py", "vault_context.py", "services.py", "states.py", "interfaces.py", 
        "usb.key", "secret.key", 
        ".DS_Store" 
    ]

    def encrypt_folder(self, folder_path: str, key: bytes) -> None:
        """
        Walks through the folder and encrypts every eligible file.
        """
        self._iterate_files(folder_path, key, mode="encrypt")

    def decrypt_folder(self, folder_path: str, key: bytes) -> None:
        """
        Walks through the folder and decrypts every eligible file.
        """
        self._iterate_files(folder_path, key, mode="decrypt")

    def _iterate_files(self, folder_path: str, key: bytes, mode: str) -> None:
        # Scan all folders and files
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                
                if file_name in self.IGNORE_FILES or file_name.endswith(".py"):
                    print(f"Skipping system file: {file_name}")
                    continue

                full_path = os.path.join(root, file_name)
                
                self._process_file(full_path, key, mode)

    def _process_file(self, file_path: str, key: bytes, mode: str) -> None:
        """
        Internal Helper: Performs the actual IO and Cryptography on a single file.
        """
        try:
            fernet = Fernet(key)
            with open(file_path, "rb") as f:
                original_data = f.read()

            if mode == "encrypt":
                processed_data = fernet.encrypt(original_data)
            else: 
                processed_data = fernet.decrypt(original_data)

            with open(file_path, "wb") as f:
                f.write(processed_data)
            
            print(f"[{mode.upper()}] Success: {os.path.basename(file_path)}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


class KeyManager:
    
    def __init__  (self, fileName= "secret.key"):
        self.key_filename = fileName
        self.key= None
    
    def load_key(self):
        if not os.path.exists(self.key_filename):
            return None
        
        with open(self.key_filename, "rb") as key_file:
            self.key = key_file.read()
            
        return self.key
    
    def generate_key(self):
        self.key = Fernet.generate_key()
        return self.key
    
    def save_key(self):
        with open(self.key_filename, "wb") as key_file:
            key_file.write(self.key)
    
    def secure_shred(self):
        if not os.path.exists(self.key_filename):
            return 
        file_size = os.path.getsize(self.key_filename)

        with open(self.key_filename, "ba+") as file:
            file.seek(0)
            file.write(b'\x00' * file_size)
            file.flush()

            file.seek(0)
            file.write(b'\xFF' * file_size)
            file.flush()

            file.seek(0)
            file.write(os.urandom(file_size))
            file.flush()
        
        os.remove(self.key_filename)
        self.key = None

class HoneyMonitor:
    def __init__(self):
        self.observer = None
        self.decoys = ["passwords.txt", "bank_info.csv", "secret_project.docx"]
    
    def deploy_decoys(self,folder_path):
        for file_name in self.decoys:
            full_path = os.path.join(folder_path, file_name)
            if not os.path.exists(full_path):
                with open(full_path, "w") as f:
                    f.write("CONFIDENTIAL DATA\n")
                    f.write("Username: admin\n")
                    f.write("Password: SuperSecretPassword123!\n")
                    f.write("Do not share outside the company.")
                
                    print(f"[HONEYPOT] Deployed trap: {file_name}")
    
    def start_monitoring(self, folder_path, callback):
        print(f"[MONITOR] Started watching: {folder_path}")
        
        event_handler = TrapHandler(self.decoys, callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, folder_path, recursive=False)
        self.observer.start()
  
    def stop_monitoring(self, allow_join=True):
        if self.observer:
            print("[MONITOR] Stopping observer...")
            self.observer.stop()
            if allow_join:
                self.observer.join()
                
            print("[MONITOR] Observer stopped.")
    
    def remove_decoys(self, folder_path):
        """Deletes the traps when the software closes."""
        print(f"--- Cleaning up decoys in {folder_path} ---")
        for file_name in self.decoys:
            full_path = os.path.join(folder_path, file_name)
            try:
                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f"[HONEYPOT] Removed: {file_name}")
            except Exception as e:
                print(f"Error removing {file_name}: {e}")

class TrapHandler(FileSystemEventHandler):
    def __init__(self,decoys,callback):
        self.decoys = decoys
        self.callback = callback
    
    def on_modified(self,event):
        if event.is_directory:
            return
        file_name = os.path.basename(event.src_path)
        if file_name in self.decoys:
            print("Intrusion detected!")
            self.callback()