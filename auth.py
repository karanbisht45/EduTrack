import sqlite3
import hashlib

DB_FILE = "students.db"

def create_user_table():
    """Create users table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

def hash_password(password: str) -> str:
    """Hash password with SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username: str, password: str) -> tuple[bool, str]:
    """Register new user."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hash_password(password)))
            conn.commit()
        return True, "Signup successful ✅"
    except sqlite3.IntegrityError:
        return False, "Username already exists ❌"

def login_user(username: str, password: str) -> bool:
    """Check user credentials."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, hash_password(password)))
        return c.fetchone() is not None
