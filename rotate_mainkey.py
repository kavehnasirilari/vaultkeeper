# rotate_mainkey.py
import base64
import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

DB_PATH = "vault.db"
TABLE = "passwords"
SALT = b"FixedSaltForMainKey123!"
VERSION = b"\x01"
NONCE_LEN = 12
ITERATIONS = 100_000

def _derive_key(key_str: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(key_str.encode("utf-8"))

def _decrypt_ppp(enc_b64: str, main_key: str) -> str:
    raw = base64.b64decode(enc_b64, validate=True)
    if raw[:1] != VERSION:
        raise ValueError("Unsupported token version.")
    nonce = raw[1:1 + NONCE_LEN]
    ct = raw[1 + NONCE_LEN:]
    aes = AESGCM(_derive_key(main_key))
    pt = aes.decrypt(nonce, ct, None)
    return pt.decode("utf-8")

def _encrypt_ppp(plaintext: str, main_key: str) -> str:
    key = _derive_key(main_key)
    nonce = os.urandom(NONCE_LEN)
    aes = AESGCM(key)
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    token = VERSION + nonce + ct
    return base64.b64encode(token).decode("ascii")

def rotate_mainkey(old_key: str, new_key: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT id, ppp FROM {TABLE}")
    rows = cur.fetchall()
    updated = 0

    for row_id, enc_ppp in rows:
        try:
            plain = _decrypt_ppp(enc_ppp, old_key)
            new_enc = _encrypt_ppp(plain, new_key)
            cur.execute(f"UPDATE {TABLE} SET ppp = ? WHERE id = ?", (new_enc, row_id))
            updated += 1
        except Exception as e:
            print(f"⚠️ Skipped id={row_id}: {e}")
            continue

    conn.commit()
    conn.close()
    print(f"✅ Done. Updated {updated} rows.")

def rotate_mainkey_cli():
    import os
    from getpass import getpass
    old_key = getpass("Enter OLD MainKey: ")
    new_key = getpass("Enter NEW MainKey: ")
    confirm = getpass("Confirm NEW MainKey: ")
    if new_key != confirm:
        print("❌ New keys do not match.")
        exit(1)

    rotate_mainkey(old_key, new_key)


if __name__ == "__main__":
    import os
    from getpass import getpass
    old_key = getpass("Enter OLD MainKey: ")
    new_key = getpass("Enter NEW MainKey: ")
    confirm = getpass("Confirm NEW MainKey: ")
    if new_key != confirm:
        print("❌ New keys do not match.")
        exit(1)

    rotate_mainkey(old_key, new_key)
