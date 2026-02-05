import time
import os
import shutil
from services import CryptoService, KeyManager

def run_benchmark():
    print("--- Starting Performance Benchmark ---")
    print(f"{'File Size':<15} | {'Encrypt Time':<15} | {'Decrypt Time':<15}")
    print("-" * 50)

    test_dir = "benchmark_env"
    os.makedirs(test_dir, exist_ok=True)
    
    crypto = CryptoService()
    key_manager = KeyManager()
    key = key_manager.generate_key()

    # checking files size 1KB, 1MB, 10MB
    sizes = [
        ("1KB", 1024), 
        ("1MB", 1024 * 1024), 
        ("10MB", 10 * 1024 * 1024)
    ]

    for label, size_bytes in sizes:
        # 1. demo files
        file_path = os.path.join(test_dir, f"test_{label}.dat")
        with open(file_path, "wb") as f:
            f.write(os.urandom(size_bytes))

        # 2. Encryption time measurement
        start_time = time.time()
        crypto.encrypt_folder(test_dir, key)
        enc_duration = time.time() - start_time

        # 3. Decoding time measurement
        start_time = time.time()
        crypto.decrypt_folder(test_dir, key)
        dec_duration = time.time() - start_time

        
        print(f"{label:<15} | {enc_duration:.5f} sec    | {dec_duration:.5f} sec")
        os.remove(file_path)

    # general cleaning
    shutil.rmtree(test_dir)
    print("-" * 50)
    print("Benchmark Complete.")

if __name__ == "__main__":
    run_benchmark()