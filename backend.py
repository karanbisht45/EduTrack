import sqlite3
from typing import List, Tuple, Optional, Dict, Any
import cohere   # ✅ Using Cohere 

# ============================= CONFIG =============================
DB_FILE = "students.db"

SCHEMA_COLUMNS = [
    "student_id", "roll_no", "name", "age", "gender", "category",
    "address", "course", "current_year", "semester",
    "type", "room_no", "hostel_building", "block", "bus_no", "route",
    "attendance"  # ✅ Added attendance
]

# ✅ Initialize Cohere Client (replace with your API key)
co = cohere.Client("your_api_key")


# ============================= DB INIT =============================
# ============================= DB INIT =============================
def create_db():
    """Create students table if not exists (no drop)."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                roll_no TEXT UNIQUE,
                name TEXT,
                age INTEGER,
                gender TEXT,
                category TEXT,
                address TEXT,
                course TEXT,
                current_year INTEGER,
                semester INTEGER,
                type TEXT,                -- Hosteller / Day Scholar
                room_no TEXT,             -- hosteller only
                hostel_building TEXT,     -- hosteller only
                block TEXT,               -- hosteller only
                bus_no TEXT,              -- day scholar only
                route TEXT,               -- day scholar only
                attendance INTEGER DEFAULT 80  -- ✅ Added attendance
            )
        """)
        conn.commit()

    # ✅ Ensure 'attendance' column exists for older DBs
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("PRAGMA table_info(students)")
        columns = [col[1] for col in c.fetchall()]
        if "attendance" not in columns:
            c.execute("ALTER TABLE students ADD COLUMN attendance INTEGER DEFAULT 80")
        conn.commit()


# ============================= INSERT =============================
def insert_student(student_id: str, roll_no: str, name: str, age: int, gender: str,
                   category: str, address: str, course: str, current_year: int,
                   semester: int, type_: str, room_no: Optional[str] = None,
                   hostel_building: Optional[str] = None, block: Optional[str] = None,
                   bus_no: Optional[str] = None, route: Optional[str] = None,
                   attendance: int = 80) -> Tuple[bool, str]:
    """Insert student, return success flag and message."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO students (
                    student_id, roll_no, name, age, gender, category, address, course, current_year, semester,
                    type, room_no, hostel_building, block, bus_no, route, attendance
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (student_id, roll_no, name, age, gender, category, address, course,
                  current_year, semester, type_, room_no, hostel_building, block, bus_no, route,
                  attendance))
            conn.commit()
        return True, "ok"
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "UNIQUE constraint failed: students.student_id" in msg:
            return False, "Student ID already exists."
        if "UNIQUE constraint failed: students.roll_no" in msg:
            return False, "Roll No already exists."
        return False, msg


# ============================= GET =============================
def get_student(student_id: str) -> Optional[Tuple]:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        return c.fetchone()


def get_student_by_roll(roll_no: str) -> Optional[Tuple]:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
        return c.fetchone()


# ============================= UPDATE =============================
def update_student(student_id: str, **kwargs) -> Tuple[bool, str]:
    """Update student fields, return success flag and message."""
    if not kwargs:
        return False, "No fields to update."
    for k in kwargs.keys():
        if k not in SCHEMA_COLUMNS or k == "student_id":
            return False, f"Invalid field: {k}"

    fields_clause = ", ".join([f"{k}=?" for k in kwargs.keys()])
    values = list(kwargs.values()) + [student_id]

    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute(f"UPDATE students SET {fields_clause} WHERE student_id=?", values)
            conn.commit()
        return True, "ok"
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "UNIQUE constraint failed: students.roll_no" in msg:
            return False, "Roll No already exists."
        return False, msg


# ============================= DELETE =============================
def delete_student(student_id: str) -> None:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        conn.commit()


# ============================= FETCH =============================
def fetch_students(filters: Optional[Dict[str, Any]] = None) -> List[Tuple]:
    """
    Fetch students with optional filters.
    filters (all optional):
      - type (list[str])
      - gender (list[str])
      - category (list[str])
      - course_contains (str)
      - name_contains (str)
      - year_in (list[int])
      - sem_in (list[int])
    """
    query = "SELECT * FROM students WHERE 1=1"
    params: List[Any] = []

    if filters:
        if filters.get("type"):
            placeholders = ",".join(["?"] * len(filters["type"]))
            query += f" AND type IN ({placeholders})"
            params += list(filters["type"])
        if filters.get("gender"):
            placeholders = ",".join(["?"] * len(filters["gender"]))
            query += f" AND gender IN ({placeholders})"
            params += list(filters["gender"])
        if filters.get("category"):
            placeholders = ",".join(["?"] * len(filters["category"]))
            query += f" AND category IN ({placeholders})"
            params += list(filters["category"])
        if filters.get("course_contains"):
            query += " AND course LIKE ?"
            params.append(f"%{filters['course_contains']}%")
        if filters.get("name_contains"):
            query += " AND name LIKE ?"
            params.append(f"%{filters['name_contains']}%")
        if filters.get("year_in"):
            placeholders = ",".join(["?"] * len(filters["year_in"]))
            query += f" AND current_year IN ({placeholders})"
            params += list(filters["year_in"])
        if filters.get("sem_in"):
            placeholders = ",".join(["?"] * len(filters["sem_in"]))
            query += f" AND semester IN ({placeholders})"
            params += list(filters["sem_in"])

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(query, tuple(params))
        return c.fetchall()


# ============================= RAW ALL =============================
def all_rows() -> List[Tuple]:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        return c.fetchall()


# ============================= ADMIN AI CHATBOT =============================
def admin_chatbot_query(query: str) -> str:
    """
    AI-powered chatbot for admin queries using Cohere.
    Converts plain English to SELECT SQL and executes safely.
    """
    try:
        prompt = f"""
        You are a SQL expert.
        Convert the following request into a valid SQLite SELECT query only
        for the 'students' table.
        Table columns: {", ".join(SCHEMA_COLUMNS)}.
        Do not generate INSERT, UPDATE, DELETE, or DROP queries.
        Request: {query}
        """

        response = co.generate(
            model="command-r-plus",  # Cohere model
            prompt=prompt,
            max_tokens=150,
            temperature=0
        )

        sql_query = response.generations[0].text.strip()

        if not sql_query.lower().startswith("select"):
            return "❌ Only SELECT queries are allowed for safety."

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        conn.close()

        if not rows:
            return "No results found."
        return str(rows)

    except Exception as e:
        return f"AI/DB Error: {e}"


# ============================= ATTENDANCE RISK PREDICTION =============================
def predict_risk(attendance: int) -> str:
    """AI-based student risk prediction based on attendance."""
    if attendance < 75:
        return "❌ At Risk (Low Attendance)"
    return "✅ Safe (Good Attendance)"

