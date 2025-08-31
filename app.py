import streamlit as st
import pandas as pd
from io import StringIO
import sqlite3
import cohere
import matplotlib.pyplot as plt

# ---------------- BACKEND & AUTH ----------------
from backend import (
    create_db, insert_student, get_student, get_student_by_roll,
    update_student, delete_student, fetch_students, all_rows
)
from auth import create_user_table, signup_user, login_user

# ================= INITIAL SETUP =================
create_db()
create_user_table()
st.set_page_config(page_title="Student DBMS", page_icon="🎓", layout="wide")

# ---------------- COHERE AI ----------------
COHERE_API_KEY = "ZDRGnW9Jbj1a6IhwjjTqNimk4BPcxM1bOSn3Hl33"
co = cohere.Client(COHERE_API_KEY)

def generate_sql(user_query: str) -> str:
    prompt = f"""
    You are an expert SQL assistant.
    Convert the following natural language request into a valid **SQLite SELECT query only**
    for the 'students' table.
    ✅ Rules:
    - Use only this schema: 
      (student_id, roll_no, name, age, gender, category, address, course, current_year, 
       semester, type, room_no, hostel_building, block, bus_no, route, attendance).
    - Always start with: SELECT ... FROM students
    - Do NOT generate INSERT, UPDATE, DELETE, CREATE, or DROP queries.
    - Do NOT include explanations, comments, or markdown.
    - Return ONLY the SQL query (one line or multi-line).
    - Always match text values case-insensitively using `COLLATE NOCASE`.
    - If the query is vague, assume the user wants *all columns*.
    - If no condition is mentioned, return a general `SELECT * FROM students;`.
    Request: {user_query}
    """
    response = co.chat(
        message=prompt,
        model="command-r",
        temperature=0
    )
    sql_query = response.text.strip()
    if sql_query.startswith("```"):
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    if not sql_query.lower().startswith("select"):
        sql_query = "SELECT * FROM students;"
    return sql_query

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "choice" not in st.session_state: st.session_state.choice = "➕ Add Student"

# ---------------- AUTHENTICATION ----------------
if not st.session_state.logged_in:
    st.title("🔐 Student DBMS - Login / Signup")
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        uname = st.text_input("Username", key="login_user")
        passwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            if login_user(uname, passwd):
                st.session_state.logged_in = True
                st.session_state.username = uname
                st.session_state.choice = "➕ Add Student"
                st.success(f"Welcome {uname} 🎉")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")
    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup", key="signup_btn"):
            ok, msg = signup_user(new_user, new_pass)
            if ok:
                st.success(msg)
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.session_state.choice = "➕ Add Student"
                st.rerun()
            else:
                st.error(msg)
else:
    # ---------------- SIDEBAR ----------------
    st.sidebar.success(f"👤 Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.choice = "➕ Add Student"
        st.rerun()

    # ================= MAIN MENU =================
    menu = st.sidebar.radio(
        "📚 Student DBMS Menu",
        ["➕ Add Student", "📋 View / Filter Students", "🔎 Search", 
         "✏️ Update", "🗑️ Delete", "🤖 AI DB Assistant", "📊 Risk Prediction"],
        index=[
            "➕ Add Student", "📋 View / Filter Students", "🔎 Search",
            "✏️ Update", "🗑️ Delete", "🤖 AI DB Assistant", "📊 Risk Prediction"
        ].index(st.session_state.choice) 
        if st.session_state.choice in ["➕ Add Student", "📋 View / Filter Students", "🔎 Search",
                                       "✏️ Update", "🗑️ Delete", "🤖 AI DB Assistant", "📊 Risk Prediction"] 
        else 0
    )
    st.session_state.choice = menu
    choice = menu

    st.title("🎓 Student Database Management System")

    # ---------------- Helpers ----------------
    def to_df(rows):
        return pd.DataFrame(rows, columns=[
            "Student ID", "Roll No", "Name", "Age", "Gender", "Category",
            "Address", "Course", "Current Year", "Semester",
            "Type", "Room No", "Hostel Building", "Block", "Bus No", "Route", "Attendance"
        ])
    def year_options(): return list(range(1, 6))
    def sem_options(): return list(range(1, 9))
    def is_hosteller(t): return t == "Hosteller"
    def is_day_scholar(t): return t == "Day Scholar"

    # ------------------ AI RISK PREDICTION ------------------
    def predict_risk(attendance: float) -> str:
        if attendance < 75: return "❌ At Risk (Low Attendance)"
        return "✅ Safe (Good Attendance)"
    def plot_attendance_distribution():
        conn = sqlite3.connect("students.db")
        c = conn.cursor()
        try:
            c.execute("SELECT name, attendance FROM students")
            data = c.fetchall()
        except sqlite3.OperationalError:
            st.warning("No 'attendance' column in DB. Skipping visualization.")
            return
        finally:
            conn.close()
        if not data: 
            st.warning("No student data available for visualization.")
            return
        names, attendance = zip(*data)
        plt.figure(figsize=(8, 5))
        plt.bar(names, attendance, color="skyblue")
        plt.axhline(75, color="red", linestyle="--", label="Risk Threshold (75%)")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Students")
        plt.ylabel("Attendance (%)")
        plt.title("Student Attendance Distribution")
        plt.legend()
        st.pyplot(plt)

    # ================= MENU CHOICES =================
    # -------------- ADD STUDENT --------------
    if choice == "➕ Add Student":
        st.subheader("➕ Add New Student")
        colA, colB, colC = st.columns(3)
        with colA:
            student_id = st.text_input("Student ID (Unique)")
            roll_no = st.text_input("Roll No (Unique)")
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1, key="add_age")
        with colB:
            gender = st.selectbox("Gender", ["Male", "Female", "Others"], key="add_gender")
            category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "Other"], key="add_cat")
            course = st.text_input("Course (e.g., B.Tech CSE)")
            address = st.text_area("Address", height=90)
        with colC:
            current_year = st.selectbox("Current Year", year_options(), key="add_year")
            semester = st.selectbox("Semester", sem_options(), key="add_sem")
            type_ = st.radio("Student Type", ["Hosteller", "Day Scholar"], key="add_type")
        room_no = hostel_building = block = bus_no = route = None
        if is_hosteller(type_):
            colH1, colH2, colH3 = st.columns(3)
            with colH1: room_no = st.text_input("Room No")
            with colH2: hostel_building = st.text_input("Hostel Building")
            with colH3: block = st.text_input("Block")
        elif is_day_scholar(type_):
            colD1, colD2 = st.columns(2)
            with colD1: bus_no = st.text_input("Bus No")
            with colD2: route = st.text_input("Route")
        attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, step=1, value=80)
        if st.button("Add Student", type="primary"):
            required = [student_id.strip(), roll_no.strip(), name.strip(), course.strip(), address.strip()]
            if not all(required):
                st.warning("Please fill all required fields: Student ID, Roll No, Name, Course, Address.")
            else:
                ok, msg = insert_student(
                    student_id.strip(), roll_no.strip(), name.strip(), int(age),
                    gender, category, address.strip(), course.strip(), int(current_year),
                    int(semester), type_, room_no, hostel_building, block, bus_no, route, attendance
                )
                if ok: st.success(f"Student '{name}' added successfully ✅")
                else: st.error(f"❌ {msg}")

    # -------------- VIEW / FILTER STUDENTS --------------
    elif choice == "📋 View / Filter Students":
        st.subheader("📋 View & Filter Students")
        with st.expander("Filters", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                type_filter = st.selectbox("Type", ["All", "Hosteller", "Day Scholar"], index=0)
                gender_filter = st.selectbox("Gender", ["All", "Male", "Female", "Others"], index=0)
            with col2:
                category_filter = st.multiselect("Category", ["General", "OBC", "SC", "ST", "Other"], default=[])
                course_filter = st.multiselect("Course", ["B.Tech", "M.Tech", "MBA", "B.Sc", "M.Sc", "Other"], default=[])
            with col3: year_filter = st.multiselect("Year", year_options(), default=[])
            with col4: sem_filter = st.multiselect("Semester", sem_options(), default=[])
            filters = {
                "type": None if type_filter == "All" else [type_filter],
                "gender": None if gender_filter == "All" else [gender_filter],
                "category": category_filter or None,
                "course_in": course_filter or None,
                "year_in": year_filter or None,
                "sem_in": sem_filter or None,
            }
        rows = fetch_students(filters)
        df = to_df(rows)
        st.write(f"Total: **{len(df)}** records")
        st.dataframe(df, use_container_width=True)
        csv_buf = StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button("⬇️ Download CSV", data=csv_buf.getvalue(), file_name="students.csv", mime="text/csv")

    # -------------- SEARCH --------------
    elif choice == "🔎 Search":
        st.subheader("🔎 Search Student")
        tab1, tab2 = st.tabs(["By Student ID", "By Roll No"])
        with tab1:
            sid = st.text_input("Student ID", key="search_sid")
            if st.button("Search by ID"):
                row = get_student(sid.strip())
                st.dataframe(to_df([row])) if row else st.warning("No student found.")
        with tab2:
            rno = st.text_input("Roll No", key="search_rno")
            if st.button("Search by Roll No"):
                row = get_student_by_roll(rno.strip())
                st.dataframe(to_df([row])) if row else st.warning("No student found.")

    # -------------- UPDATE --------------
    elif choice == "✏️ Update":
        st.subheader("✏️ Update Student")
        if "upd_student" not in st.session_state: st.session_state.upd_student = None
        sid = st.text_input("Enter Student ID to update", key="upd_sid")
        if st.button("Fetch", key="upd_fetch"):
            row = get_student(sid.strip())
            st.session_state.upd_student = row if row else None
            if not row: st.error("Student not found.")
        if st.session_state.upd_student:
            (
                student_id, roll_no, name, age, gender, category, address, course,
                current_year, semester, type_, room_no, hostel_building, block, bus_no, route, attendance
            ) = st.session_state.upd_student
            colA, colB, colC = st.columns(3)
            with colA:
                new_roll = st.text_input("Roll No (Unique)", value=roll_no, key="upd_roll")
                new_name = st.text_input("Full Name", value=name, key="upd_name")
                new_age = st.number_input("Age", min_value=1, max_value=120, value=int(age or 1), key="upd_age")
            with colB:
                new_gender = st.selectbox("Gender", ["Male", "Female", "Others"],
                                          index=["Male", "Female", "Others"].index(gender or "Male"), key="upd_gender")
                new_category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "Other"],
                                            index=["General", "OBC", "SC", "ST", "Other"].index(category or "General"),
                                            key="upd_cat")
                new_course = st.text_input("Course", value=course or "", key="upd_course")
            with colC:
                new_address = st.text_area("Address", value=address or "", height=90, key="upd_addr")
                new_year = st.selectbox("Current Year", year_options(),
                                        index=year_options().index(int(current_year)) if current_year in year_options() else 0,
                                        key="upd_year")
                new_sem = st.selectbox("Semester", sem_options(),
                                       index=sem_options().index(int(semester)) if semester in sem_options() else 0,
                                       key="upd_sem")
            new_type = st.radio("Student Type", ["Hosteller", "Day Scholar"],
                                index=["Hosteller", "Day Scholar"].index(type_ or "Hosteller"), key="upd_type")
            new_room = new_hostel = new_block = new_bus = new_route = None
            if new_type == "Hosteller":
                colH1, colH2, colH3 = st.columns(3)
                with colH1: new_room = st.text_input("Room No", value=room_no or "", key="upd_room")
                with colH2: new_hostel = st.text_input("Hostel Building", value=hostel_building or "", key="upd_hostel")
                with colH3: new_block = st.text_input("Block", value=block or "", key="upd_block")
            else:
                colD1, colD2 = st.columns(2)
                with colD1: new_bus = st.text_input("Bus No", value=bus_no or "", key="upd_bus")
                with colD2: new_route = st.text_input("Route", value=route or "", key="upd_route")
            new_attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, value=int(attendance or 80), key="upd_att")
            if st.button("Save Changes", type="primary", key="upd_save"):
                fields = {
                    "roll_no": new_roll.strip(),
                    "name": new_name.strip(),
                    "age": int(new_age),
                    "gender": new_gender,
                    "category": new_category,
                    "address": new_address.strip(),
                    "course": new_course.strip(),
                    "current_year": int(new_year),
                    "semester": int(new_sem),
                    "type": new_type,
                    "room_no": new_room,
                    "hostel_building": new_hostel,
                    "block": new_block,
                    "bus_no": new_bus,
                    "route": new_route,
                    "attendance": new_attendance
                }
                ok, msg = update_student(student_id, **fields)
                if ok:
                    st.success("Student updated successfully ✅")
                    st.session_state.upd_student = None
                else:
                    st.error(f"❌ {msg}")

    # -------------- DELETE --------------
    elif choice == "🗑️ Delete":
        st.subheader("🗑️ Delete Student")
        sid = st.text_input("Student ID to delete", key="del_sid")
        confirm = st.checkbox("I'm sure", key="del_confirm")
        if st.button("Delete", type="secondary", key="del_btn"):
            if not confirm: st.warning("Please confirm deletion.")
            else:
                row = get_student(sid.strip())
                if not row: st.error("Student ID not found.")
                else:
                    delete_student(sid.strip())
                    st.success("Record deleted ✅")

    # -------------- AI DB ASSISTANT --------------
    elif choice == "🤖 AI DB Assistant":
        st.subheader("🤖 AI Database Assistant (Cohere)")
        user_query = st.text_input("Enter your query (e.g., Show all hostellers in 2nd year):")
        if st.button("Run Query", type="primary", key="ai_query_btn") and user_query:
            sql_query = generate_sql(user_query).strip()
            sql_query = sql_query.split(";")[0].strip()
            if not sql_query.lower().startswith("select"):
                st.error(f"❌ Only SELECT queries are allowed. (Got: {sql_query})")
            else:
                st.write("📄 Generated SQL:", sql_query)
                conn = sqlite3.connect("students.db")
                try:
                    df = pd.read_sql_query(sql_query, conn)
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No results found.")
                except Exception as e:
                    st.error(f"SQL Error: {e}")
                finally:
                    conn.close()

    # -------------- RISK PREDICTION --------------
    elif choice == "📊 Risk Prediction":
        st.subheader("📊 AI Attendance Risk Prediction")
        sid = st.text_input("Enter Student ID to check attendance risk", key="risk_sid")
        if st.button("Predict Risk", key="risk_btn"):
            row = get_student(sid.strip())
            if not row:
                st.error("Student not found ❌")
            else:
                attendance = row[16] if len(row) > 16 and row[16] is not None else 80
                risk_status = predict_risk(attendance)
                st.markdown(f"**Student:** {row[2]} ({row[1]})")
                st.markdown(f"**Attendance:** {attendance}%")
                st.markdown(f"**Risk Status:** {risk_status}")
                st.subheader("📈 Attendance Distribution")
                plot_attendance_distribution()
