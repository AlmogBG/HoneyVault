import unittest
import os
import shutil
from services import CryptoService, KeyManager
from cryptography.fernet import Fernet

class TestHoneyVault(unittest.TestCase):
    
    def setUp(self):
        """
       This function runs before each test.
It prepares a temporary test folder and a dummy file.
        """
        self.test_dir = "test_env"
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.test_file_path = os.path.join(self.test_dir, "secret.txt")
        self.original_content = b"This is super secret data!"
        
        # Creating a source file
        with open(self.test_file_path, "wb") as f:
            f.write(self.original_content)
            
        self.crypto = CryptoService()
        self.key_manager = KeyManager(os.path.join(self.test_dir, "test.key"))

    def tearDown(self):
        """This function runs after each test.
It deletes all temporary files we created (cleanup)."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_encryption_round_trip(self):
        """
        Encryption and decryption
        """
        # 1. generate key
        key = self.key_manager.generate_key()
        
        # 2. Encryption
        self.crypto.encrypt_folder(self.test_dir, key)
        
        # checking if the file change
        with open(self.test_file_path, "rb") as f:
            encrypted_content = f.read()
        self.assertNotEqual(encrypted_content, self.original_content, "File should be encrypted now!")
        
        # 3. decryption
        self.crypto.decrypt_folder(self.test_dir, key)
        
        with open(self.test_file_path, "rb") as f:
            decrypted_content = f.read()
        self.assertEqual(decrypted_content, self.original_content, "Decryption failed to restore original data!")

    def test_key_shredding(self):
        """
       deleting key
        """
        
        self.key_manager.generate_key()
        self.key_manager.save_key()
        
        #Verifying that the file exists
        self.assertTrue(os.path.exists(self.key_manager.key_filename))
         
        self.key_manager.secure_shred()
        
        # Verifying that the file is gone 
        self.assertFalse(os.path.exists(self.key_manager.key_filename), "Key file was not deleted!")

    def test_decryption_with_wrong_key(self):
        """
        Attempting to decrypt with an incorrect key.
        The system should fail to decrypt, and the file should remain encrypted.
        """
        # Encryption with a valid key
        key_correct = self.key_manager.generate_key()
        self.crypto.encrypt_folder(self.test_dir, key_correct)
        
        # Creating a completely different key  
        key_wrong = Fernet.generate_key()
        
        # Decryption attempt with the wrong key
        self.crypto.decrypt_folder(self.test_dir, key_wrong)
        
        #  checking if the file is still encrypted.
        with open(self.test_file_path, "rb") as f:
            content = f.read()
            
        self.assertNotEqual(content, self.original_content, "Security breach! File decrypted with wrong key!")

    def test_ignored_files_safety(self):
        """
        Making sure the system doesn't touch files it shouldn't
        """
        # Creating a file that should be on the ignore list
        ignored_filename = "secret.key"
        ignored_path = os.path.join(self.test_dir, ignored_filename)
        safe_content = b"DO NOT TOUCH ME"
        
        with open(ignored_path, "wb") as f:
            f.write(safe_content)
            
        # decrypting the folder
        key = self.key_manager.generate_key()
        self.crypto.encrypt_folder(self.test_dir, key)
        
        # the "secret.key" shouldn't change
        with open(ignored_path, "rb") as f:
            current_content = f.read()
            
        self.assertEqual(current_content, safe_content, "System corrupted a protected system file!")

    def test_empty_folder(self):
        """
        Crash resistance on empty folder
        """
        empty_dir = os.path.join(self.test_dir, "empty_subfolder")
        os.makedirs(empty_dir, exist_ok=True)
        
        key = self.key_manager.generate_key()
        
        try:
            self.crypto.encrypt_folder(empty_dir, key)
            self.crypto.decrypt_folder(empty_dir, key)
        except Exception as e:
            self.fail(f"System crashed on empty folder: {e}")

if __name__ == '__main__':
    unittest.main()