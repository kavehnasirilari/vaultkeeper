# db_ops.py
from __future__ import annotations
import sqlite3
from typing import Optional, List, Tuple

DB_PATH = "vault.db"
TABLE = "passwords"

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            item VARCHAR(100) NOT NULL,
            ppp  VARCHAR(500) NOT NULL,
            use  VARCHAR(100),
            note VARCHAR(200)
        )
    """)
    return conn

def insert_row(item: str, ppp: str, use: Optional[str] = None, note: Optional[str] = None) -> int:
    """درج رکورد جدید و برگرداندن id."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {TABLE} (item, ppp, use, note) VALUES (?, ?, ?, ?)",
            (item, ppp, use, note),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def update_row(row_id: int,
               item: Optional[str] = None,
               ppp: Optional[str]  = None,
               use: Optional[str]  = None,
               note: Optional[str] = None) -> int:
    """آپدیت فیلدهای دلخواهِ یک ردیف بر اساس id. خروجی: تعداد ردیف‌های آپدیت شده."""
    fields = []
    values = []
    if item is not None:
        fields.append("item = ?"); values.append(item)
    if ppp is not None:
        fields.append("ppp = ?"); values.append(ppp)
    if use is not None:
        fields.append("use = ?"); values.append(use)
    if note is not None:
        fields.append("note = ?"); values.append(note)

    if not fields:
        return 0  # چیزی برای آپدیت نیست

    values.append(row_id)

    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE {TABLE} SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()

def Give_Items() -> List[Tuple[int, str]]:
    """لیست (id, item) همهٔ رکوردها."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id, item FROM {TABLE} ORDER BY id DESC")
        return cur.fetchall()
    finally:
        conn.close()

def Give_PPP(row_id: int) -> str:
    """برگرداندن مقدار ppp برای id داده‌شده. اگر نبود، خطا می‌دهد."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT ppp FROM {TABLE} WHERE id = ?", (row_id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Row id {row_id} not found")
        return row[0]
    finally:
        conn.close()

if __name__ == "__main__":
    # تست خیلی ساده (اختیاری)
    rid = insert_row("gmail", "BASE64_TOKEN_HERE", "myuser@gmail.com", "first record")
    print("inserted id:", rid)
    print("items:", Give_Items())
    print("ppp:", Give_PPP(rid))
    print("updated:", update_row(rid, note="updated note"))
