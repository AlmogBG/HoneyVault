🛡️ HoneyVault: Active Ransomware Defense System
HoneyVault is an active cybersecurity defense system for a personal file vault. It combines robust encryption with "Honey Traps" (Decoy files) to provide real-time detection and autonomous response against Ransomware attacks.

🚀 About the Project
Unlike standard file vaults that rely solely on passive encryption, HoneyVault actively monitors the file system. The system scatters decoy files within the protected directory. If an unauthorized entity (such as ransomware or a malicious actor) attempts to modify or access these traps, the system detects it instantly and automatically locks all genuine files under a new, secure encryption key.

🛠️ Technologies & Tools
Programming Language: Python 3.x

Encryption: cryptography library (Fernet protocol implementing AES-128 and HMAC authentication).

System Monitoring: watchdog library for real-time Kernel-level event detection.

UI Framework: Tkinter for a lightweight and responsive graphical user interface.

Key Management: Custom Secure Shredding mechanism to prevent forensic recovery of keys.

🏗️ System Architecture
The system is built with three core layers to ensure separation of concerns:

Crypto Service: Handles the mathematical logic of encryption, decryption, and physical key shredding.

Honey Monitor: A thread-based component utilizing the Observer Pattern to listen for file system events without blocking the UI.

Vault Context (Orchestrator): The "Brain" of the system that synchronizes detection with response and manages the vault states (Locked/Unlocked).

✨ Key Features
Active Intrusion Detection: Triggering a "Panic Mode" within milliseconds of a trap being touched.

Secure Shredding: Physical destruction of the encryption key from the disk by overwriting it with zeros.

Automated Key Rotation: Generating a fresh key during an emergency lockdown to stay ahead of the attacker.

Graceful Shutdown: Ensures all background monitors are terminated correctly to prevent resource leaks.

Performance Benchmarking: Built-in tool to measure encryption latency across various data volumes.

📥 Installation & Usage
Clone the repository:

Bash
git clone https://github.com/your-username/HoneyVault.git
Install dependencies:

Bash
pip install cryptography watchdog
Run the application:

Bash
python main.py
📊 Experimental Results (Scalability)
During development, performance benchmarks were conducted to ensure system stability. Testing showed that encryption time scales linearly relative to file volume. The system is highly efficient for documents and images, maintaining a response time of less than 1.0s under standard workloads.

Academic Note: This project was developed as part of a Cybersecurity course to demonstrate the integration of proactive defense strategies with modern cryptographic management.
