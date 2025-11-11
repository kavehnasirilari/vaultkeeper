import sqlite3

DB_PATH = "vault.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item VARCHAR(100) NOT NULL,
        ppp  VARCHAR(500) NOT NULL,
        use  VARCHAR(100),
        note VARCHAR(200)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database & table created successfully.")

if __name__ == "__main__":
    init_db()
