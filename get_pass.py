# get_pass.py
import base64, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from db_ops import Give_PPP  # returns encrypted PPP (base64) by row_id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT = b"FixedSaltForMainKey123!"  # طولانی و ثابت ولی عمومی

VERSION = b"\x01"
NONCE_LEN = 12

# def _derive_key(key_str: str) -> bytes:
#     return hashlib.sha256(key_str.encode("utf-8")).digest()

def _derive_key(master_key: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(master_key.encode("utf-8"))

def _decrypt_with_key(token_b64: str, key_str: str) -> str:
    raw = base64.b64decode(token_b64, validate=True)
    if len(raw) < 1 + NONCE_LEN + 16:
        raise ValueError("Token is too short or corrupted.")
    if raw[0:1] != VERSION:
        raise ValueError("Unsupported token version.")
    nonce = raw[1:1+NONCE_LEN]
    ct = raw[1+NONCE_LEN:]
    key = _derive_key(key_str)
    pt = AESGCM(key).decrypt(nonce, ct, None)
    return pt.decode("utf-8")

def Give_Pass(row_id: int, MainKey: str) -> str:
    """Fetch PPP by id and return the decrypted password (plaintext)."""
    enc_ppp = Give_PPP(row_id)     # base64 token from DB
    return _decrypt_with_key(enc_ppp, MainKey)
