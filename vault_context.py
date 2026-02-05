import os
import time
from services import CryptoService, KeyManager, HoneyMonitor

class VaultContext:
    def __init__(self):
        self.root_folder = None
        self.is_locked = True
        self.crypto = CryptoService()
        self.key_manager = KeyManager()
        self.monitor = HoneyMonitor()

    def set_vault_path(self, path):
        self.root_folder = path
        self.is_locked = False 
        self.monitor.deploy_decoys(path)
    
    def lock_vault(self):
        if not self.root_folder:
            print("root folder not found")
            return
        print("Pausing monitor for encryption...")
        if self.monitor:
            self.monitor.stop_monitoring()

        key = self.key_manager.generate_key()
        self.key_manager.save_key()
        
        self.crypto.encrypt_folder(self.root_folder, key)
        
        self.is_locked = True
        print("vault locked successfully")
    
    def unlock_vault(self):
        if not self.root_folder:
            print("root folder not found")
            return
            
        key = self.key_manager.load_key()
        if key is None:
            print("No key found! Cannot unlock")
            return
            
        self.crypto.decrypt_folder(self.root_folder, key)
        
        self.key_manager.secure_shred()
        self.is_locked = False
        print("Vault unlocked and key destroyed")
        print("Resuming protection...")
        self.monitor.start_monitoring(self.root_folder, self.handle_breach)
    
    def handle_breach(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("HONEYPOT TRIGGERED!")
        print("Initiating EMERGENCY LOCKDOWN!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        if not self.is_locked:
            self.emergency_lockdown()
    
    def start_protection(self):
       if self.root_folder:
            self.monitor.start_monitoring(self.root_folder, self.handle_breach)

    def stop_services(self):
        print("--- Stopping Services... ---")
        if self.monitor:
            self.monitor.stop_monitoring()
        
        if self.root_folder:
            try:
                print(f"Removing decoys from: {self.root_folder}")
                self.monitor.remove_decoys(self.root_folder)
            except Exception as e:
                print(f"Cleanup error: {e}")

    def emergency_lockdown(self):
        print("--- PANIC MODE: LOCKING EVERYTHING ---")
        if self.monitor:
            self.monitor.stop_monitoring(allow_join=False)
            
        key = self.key_manager.generate_key()
        self.key_manager.save_key()
        
        try:
            self.crypto.encrypt_folder(self.root_folder, key)
            self.is_locked = True
            print("[DEFENSE] Threat neutralized. Vault is now LOCKED.")
        except Exception as e:
            print(f"ERROR in Lockdown: {e}")