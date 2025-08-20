# 🎓 EduTrack — Student Database Management System (DBMS)

![Repo Stars](https://img.shields.io/github/stars/karanbisht45/EduTrack?style=social)
![Forks](https://img.shields.io/github/forks/karanbisht45/EduTrack?style=social)
![Issues](https://img.shields.io/github/issues/karanbisht45/EduTrack)
![License](https://img.shields.io/github/license/karanbisht45/EduTrack)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Powered%20By-Streamlit-ff4b4b?logo=streamlit)

---

## 🖥️ Demo Preview  

👉 *How EduTrack looks in action:*  

![EduTrack Demo](assets/demo.gif)  
*(Add your screenshots/GIF in `assets/` folder and update the path)*  

---

## ✨ Features

- ➕ **Add Students** — Insert records with details like ID, Roll No, Name, Course, Address, Year, Semester, and Type  
- 📋 **View & Filter** — Filter students by gender, category, year, semester, course, or type (Hosteller / Day Scholar)  
- 🔎 **Search** — Look up students instantly by *Student ID* or *Roll No*  
- ✏️ **Update Records** — Modify student details with inline editable forms  
- 🗑️ **Delete Students** — Secure deletion with confirmation checkbox  
- 🏨 **Hosteller / Day Scholar Support** — Hostel info (Room, Building, Block) and Bus info (Bus No, Route) managed dynamically  
- 📂 **Export to CSV** — Download filtered data instantly  
- ⚡ **Lightweight & Fast** — No external DB setup, just SQLite + Python 

---

Frontend/UI: Streamlit
Backend: Python
Database: SQLite (local file students.db)
Libraries: Pandas, IO, sqlite3

---

EduTrack/
│── app.py              # Main Streamlit UI (CRUD + Filters + Export)
│── backend.py          # Database functions (CRUD operations, filters)
│── students.db         # SQLite database (auto-created)
│── assets/             # Place screenshots / demo GIFs here
│── README.md           # Documentation

