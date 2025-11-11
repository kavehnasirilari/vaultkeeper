# insert_logic.py
import os, base64, hashlib
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# 👇 اضافه شد: ایمپورت از db_ops برای درج در دیتابیس
from db_ops import insert_row as db_insert_row

SALT = b"FixedSaltForMainKey123!"  # طولانی و ثابت ولی عمومی

VERSION = b"\x01"
NONCE_LEN = 12

# def _derive_key(master_key: str) -> bytes:
#     return hashlib.sha256(master_key.encode("utf-8")).digest()

def _derive_key(master_key: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(master_key.encode("utf-8"))

def _encrypt_with_key(plaintext: str, key_str: str) -> str:
    key = _derive_key(key_str)
    nonce = os.urandom(NONCE_LEN)
    aes = AESGCM(key)
    safe_text = plaintext.encode("utf-8", "ignore").decode("utf-8", "ignore")
    ct = aes.encrypt(nonce, safe_text.encode("utf-8"), None)
    # ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    token = VERSION + nonce + ct
    return base64.b64encode(token).decode("ascii")

def insert_row(item: str,
               use: Optional[str],
               Pass: str,
               shortKey: str,
               MainKey: str,
               note: Optional[str]) -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Encrypt fields according to the rule and return:
    (enc_item, enc_ppp, enc_use, enc_note)
    """
    enc_item = _encrypt_with_key(item, shortKey)
    enc_ppp  = _encrypt_with_key(Pass, MainKey)
    enc_use  = _encrypt_with_key(use, shortKey) if use else None
    enc_note = _encrypt_with_key(note, shortKey) if note else None
    return enc_item, enc_ppp, enc_use, enc_note

# 👇 تابع جدید: رمزگذاری + درج مستقیم در دیتابیس
def encrypt_and_store(item: str,
                      use: Optional[str],
                      Pass: str,
                      shortKey: str,
                      MainKey: str,
                      note: Optional[str]) -> int:
    """
    Encrypts (item/use/note) with shortKey and Pass with MainKey,
    then inserts into the 'passwords' table via db_ops.insert_row.
    Returns: inserted row id (int)
    """
    enc_item, enc_ppp, enc_use, enc_note = insert_row(
        item=item, use=use, Pass=Pass, shortKey=shortKey, MainKey=MainKey, note=note
    )
    # db_ops.insert_row expects (item, ppp, use, note) → already encrypted values
    row_id = db_insert_row(enc_item, enc_ppp, enc_use, enc_note)
    return row_id
