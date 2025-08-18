import streamlit as st
import pandas as pd
from io import StringIO
from backend import (
    create_db, insert_student, get_student, get_student_by_roll,
    update_student, delete_student, fetch_students, all_rows, SCHEMA_COLUMNS
)

# Initialize DB
create_db()

st.set_page_config(page_title="Student DBMS", page_icon="🎓", layout="wide")
st.title("🎓 Student Database Management System")

import streamlit as st

st.sidebar.title("📚 Student DBMS Menu")

if st.sidebar.button("➕ Add Student"):
    choice = "Add Student"
elif st.sidebar.button("📋 View / Filter Students"):
    choice = "View / Filter Students"
elif st.sidebar.button("🔎 Search"):
    choice = "Search"
elif st.sidebar.button("✏️ Update"):
    choice = "Update"
elif st.sidebar.button("🗑️ Delete"):
    choice = "Delete"
else:
    choice = "Add Student"  # default



# Helpers
def to_df(rows):
    return pd.DataFrame(rows, columns=[
        "Student ID", "Roll No", "Name", "Age", "Gender", "Category",
        "Address", "Course", "Current Year", "Semester",
        "Type", "Room No", "Hostel Building", "Block", "Bus No", "Route"
    ])

def year_options():
    return list(range(1, 6))  # 1..5

def sem_options():
    return list(range(1, 9))  # 1..8

def is_hosteller(t): return t == "Hosteller"
def is_day_scholar(t): return t == "Day Scholar"

# =============== ADD STUDENT ===============
if choice == "Add Student":
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

    # Conditional fields
    room_no = hostel_building = block = bus_no = route = None

    if is_hosteller(type_):
        colH1, colH2, colH3 = st.columns(3)
        with colH1:
            room_no = st.text_input("Room No")
        with colH2:
            hostel_building = st.text_input("Hostel Building")
        with colH3:
            block = st.text_input("Block")
    elif is_day_scholar(type_):
        colD1, colD2 = st.columns(2)
        with colD1:
            bus_no = st.text_input("Bus No")
        with colD2:
            route = st.text_input("Route")

    if st.button("Add Student", type="primary"):
        required = [student_id.strip(), roll_no.strip(), name.strip(), course.strip(), address.strip()]
        if not all(required):
            st.warning("Please fill all required fields: Student ID, Roll No, Name, Course, Address.")
        else:
            ok, msg = insert_student(
                student_id.strip(), roll_no.strip(), name.strip(), int(age),
                gender, category, address.strip(), course.strip(), int(current_year),
                int(semester), type_, room_no, hostel_building, block, bus_no, route
            )
            if ok:
                st.success(f"Student '{name}' added successfully ✅")
            else:
                st.error(f"❌ {msg}")

# =============== VIEW / FILTER ===============
elif choice == "View / Filter Students":
    st.subheader("📋 View & Filter Students")

    with st.expander("Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            type_filter = st.selectbox("Type", ["All", "Hosteller", "Day Scholar"], index=0)
            gender_filter = st.selectbox("Gender", ["All", "Male", "Female", "Others"], index=0)

        with col2:
            category_filter = st.multiselect("Category", ["General", "OBC", "SC", "ST", "Other"], default=[])
            course_filter = st.multiselect("Course", 
                                           ["B.Tech", "M.Tech", "MBA", "B.Sc", "M.Sc", "Other"], 
                                           default=[])

        with col3:
            year_filter = st.multiselect("Year", year_options(), default=[])

        with col4:
            sem_filter = st.multiselect("Semester", sem_options(), default=[])

        # Collect all filters
        filters = {
            "type": None if type_filter == "All" else [type_filter],
            "gender": None if gender_filter == "All" else [gender_filter],
            "category": category_filter or None,
            "course_in": course_filter or None,   # ✅ proper dropdown filter
            "year_in": year_filter or None,
            "sem_in": sem_filter or None,
        }

    # Fetch and display
    rows = fetch_students(filters)
    df = to_df(rows)

    st.write(f"Total: **{len(df)}** records")
    st.dataframe(df, use_container_width=True)


    # Download CSV
    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("⬇️ Download CSV", data=csv_buf.getvalue(), file_name="students.csv", mime="text/csv")

# =============== SEARCH ===============
elif choice == "Search":
    st.subheader("🔎 Search Student")

    tab1, tab2 = st.tabs(["By Student ID", "By Roll No"])
    with tab1:
        sid = st.text_input("Student ID", key="search_sid")
        if st.button("Search by ID"):
            row = get_student(sid.strip())
            if row:
                st.dataframe(to_df([row]))
            else:
                st.warning("No student found with that Student ID.")
    with tab2:
        rno = st.text_input("Roll No", key="search_rno")
        if st.button("Search by Roll No"):
            row = get_student_by_roll(rno.strip())
            if row:
                st.dataframe(to_df([row]))
            else:
                st.warning("No student found with that Roll No.")

# =============== UPDATE ===============
elif choice == "Update":
    st.subheader("✏️ Update Student")

    # Keep selected student in session
    if "upd_student" not in st.session_state:
        st.session_state.upd_student = None

    sid = st.text_input("Enter Student ID to update", key="upd_sid")

    if st.button("Fetch", key="upd_fetch"):
        row = get_student(sid.strip())
        if not row:
            st.error("Student not found.")
            st.session_state.upd_student = None
        else:
            st.session_state.upd_student = row  # ✅ Store in session_state

    if st.session_state.upd_student:
        (
            student_id, roll_no, name, age, gender, category, address, course,
            current_year, semester, type_, room_no, hostel_building, block, bus_no, route
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
            with colH1:
                new_room = st.text_input("Room No", value=room_no or "", key="upd_room")
            with colH2:
                new_hostel = st.text_input("Hostel Building", value=hostel_building or "", key="upd_hostel")
            with colH3:
                new_block = st.text_input("Block", value=block or "", key="upd_block")
        else:
            colD1, colD2 = st.columns(2)
            with colD1:
                new_bus = st.text_input("Bus No", value=bus_no or "", key="upd_bus")
            with colD2:
                new_route = st.text_input("Route", value=route or "", key="upd_route")

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
                "route": new_route
            }
            ok, msg = update_student(student_id, **fields)
            if ok:
                st.success("Student updated successfully ✅")
                st.session_state.upd_student = None  # clear after save
            else:
                st.error(f"❌ {msg}")


# =============== DELETE ===============
elif choice == "Delete":
    st.subheader("🗑️ Delete Student")
    sid = st.text_input("Student ID to delete", key="del_sid")
    col1, col2 = st.columns([1, 2])
    with col1:
        confirm = st.checkbox("I'm sure", key="del_confirm")
    with col2:
        if st.button("Delete", type="secondary", key="del_btn"):
            if not confirm:
                st.warning("Please confirm deletion.")
            else:
                row = get_student(sid.strip())
                if not row:
                    st.error("Student ID not found.")
                else:
                    delete_student(sid.strip())
                    st.success("Record deleted ✅")
