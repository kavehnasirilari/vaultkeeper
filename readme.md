# 🧩 VaultKeeper  
**A simple encrypted vault for your secrets, built for developers.**  
by [@kavehnasirilari](https://github.com/kavehnasirilari)

---

## 🔐 Overview
VaultKeeper is a lightweight, offline password manager written in **Python**.  
It uses **AES-GCM** encryption and **Argon2/PBKDF2-HMAC-SHA256** key derivation to securely store and retrieve your passwords in a local **SQLite** database — no cloud, no tracking, no dependencies on third-party services.

All encryption happens locally on your machine.  
Only your **Main Key** can decrypt the database — without it, recovery is mathematically infeasible.

---

## ⚙️ Features
- 🔒 **Strong encryption:** AES-256-GCM with unique nonce per record.  
- 🧠 **Key derivation:** PBKDF2-HMAC-SHA256 (100k iterations, fixed public salt).  
- 🗝️ **Dual-key system:**  
  - `MainKey` encrypts actual passwords.  
  - `shortKey` encrypts metadata (`item`, `use`, `note`).  
- 💾 **SQLite backend** — portable, simple, local file.  
- 💻 **CLI-based interface** (runs on Linux, macOS, Windows, and Termux).  
- 🔍 **Search and view items easily** with optional decryption preview.  
- 🧹 **Clean, auditable codebase** with no telemetry or analytics.  
- 🧰 **Extensible architecture** — easy to add UI or export modules later.

---

## 🧱 Project Structure

vaultkeeper/
├── main.py # CLI menu and interactive input
├── db_ops.py # Database layer (insert, update, query)
├── insert_logic.py # Encryption and secure insert logic
├── give_items.py # List/decrypt records using shortKey
├── get_pass.py # Decrypt password (ppp) using MainKey
├── init_db.py # Create initial vault.db structure
├── requirements.txt
└── vault.db # Local encrypted database




---

## 🚀 Getting Started

### 1️⃣ Clone and Setup
```bash
git clone https://github.com/kavehnasirilari/vaultkeeper.git
cd vaultkeeper
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
pip install -r requirements.txt


2️⃣ Initialize the Database
python init_db.py

3️⃣ Run the Vault
python main.py


Typical flow in menu:
1) Insert a new record
2) Update an existing record
3) List all items
4) Get password by ID
0) Exit




🧩 Credits

Developed by Kaveh Nasiri Lari

Built for developers who prefer local encryption, total control, and simplicity.
