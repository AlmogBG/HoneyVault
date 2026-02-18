# 🛡️ HoneyVault: Active Ransomware Defense System

**HoneyVault** is an active cybersecurity defense system for a personal file vault. It combines robust encryption with "Honey Traps" (Decoy files) to provide real-time detection and autonomous response against Ransomware attacks.

---

## 🚀 Project Overview
Unlike standard file vaults that rely solely on passive encryption, **HoneyVault** actively monitors the file system for threats.

* **Proactive Defense**: The system scatters decoy files within the protected directory.
* **Instant Detection**: If an unauthorized entity (ransomware/malicious actor) modifies these traps, the system detects it instantly.
* **Autonomous Response**: Upon detection, the system automatically locks all genuine files under a new, secure encryption key.

## 🛠️ Technologies & Tools
* **Programming Language**: Python 3.x
* **Encryption**: `cryptography` library (Fernet protocol: AES-128 + HMAC authentication).
* **System Monitoring**: `watchdog` library for Kernel-level event detection.
* **GUI Framework**: `Tkinter` for a responsive user interface.
* **Key Security**: Custom **Secure Shredding** mechanism to prevent forensic recovery.

## 🏗️ System Architecture
The system follows a modular design to ensure clear separation of concerns:

| Component | Responsibility |
| :--- | :--- |
| **Crypto Service** | Mathematical logic for encryption, decryption, and key shredding. |
| **Honey Monitor** | Background thread utilizing the **Observer Pattern** to listen for events. |
| **Vault Context** | The "Brain" that orchestrates states and triggers emergency lockdowns. |

## ✨ Key Features
* ⚡ **Panic Mode**: Triggered within milliseconds of an intrusion.
* ♻️ **Key Rotation**: Generates a fresh key during every emergency event.
* 🧹 **Graceful Shutdown**: Ensures all background processes are cleaned up.
* 📈 **Benchmarking**: Built-in tool to measure encryption latency across different data loads.

## 📥 Installation
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/AlmogBG/HoneyVault.git](https://github.com/AlmogBG/HoneyVault.git)
