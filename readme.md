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

