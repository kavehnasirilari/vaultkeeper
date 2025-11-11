# give_items.py (fixed)
from __future__ import annotations
import base64, sqlite3
from typing import Optional, List, Tuple
import pandas as pd

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

DB_PATH = "vault.db"
TABLE = "passwords"

# MUST match insert_logic.py
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

def _try_decrypt(token_b64: Optional[str], key_str: str) -> Optional[str]:
    if not token_b64:
        return None
    try:
        raw = base64.b64decode(token_b64, validate=True)
        if len(raw) < 1 + NONCE_LEN + 16:   # version + nonce + tag+ct
            return "<encrypted>"
        if raw[:1] != VERSION:
            return "<encrypted>"
        nonce = raw[1:1+NONCE_LEN]
        ct = raw[1+NONCE_LEN:]
        aes = AESGCM(_derive_key(key_str))
        pt = aes.decrypt(nonce, ct, None)
        return pt.decode("utf-8")
    except (InvalidTag, ValueError, base64.binascii.Error):
        return "<encrypted>"

def Give_Items(shortKey: str) -> pd.DataFrame:
    """
    Decrypt item/use/note with shortKey. If decrypt fails, show '<encrypted>'.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id, item, use, note FROM {TABLE} ORDER BY id DESC")
        rows: List[Tuple[int, Optional[str], Optional[str], Optional[str]]] = cur.fetchall()
    finally:
        conn.close()

    out = []
    for rid, v_item, v_use, v_note in rows:
        out.append({
            "id": rid,
            "item": _try_decrypt(v_item, shortKey),
            "use":  _try_decrypt(v_use,  shortKey),
            "note": _try_decrypt(v_note, shortKey),
        })
    return pd.DataFrame(out, columns=["id", "item", "use", "note"])


