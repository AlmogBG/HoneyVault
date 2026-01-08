from cryptography.fernet import Fernet
import os
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as file:
            file.write(key)

def load_key():
    with open("secret.key", "rb") as file:
            key = file.read()
    return key

def encrypt_file(file_name):
    my_key = load_key()
    f = Fernet(my_key)
    with open(file_name, "rb") as file:
            file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
            file.write(encrypted_data)

def decrypt_file(file_name):
    my_key = load_key()
    f = Fernet(my_key)
    with open(file_name, "rb") as file:
            file_data = file.read()
    decrypted_data = f.decrypt(file_data)
    with open(file_name, "wb") as file:
            file.write(decrypted_data)
generate_key()
encrypt_file("test.txt")
decrypt_file("test.txt")