# 🎓 EduTrack — Student Database Management System (DBMS)

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Powered%20By-Streamlit-ff4b4b?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Database-SQLite-green?logo=sqlite" alt="SQLite">
</p>

---

## 🌟 Overview  
EduTrack is a **Student Database Management System (DBMS)** built with **Python + Streamlit**.  
It provides a simple yet powerful interface for managing student records — including **CRUD operations**, **filters**, **search**, and **hosteller/day-scholar support** — all backed by an **SQLite database**.

---

## ✨ Features  

- ➕ **Add Students** — Insert records with details like ID, Roll No, Name, Course, Address, Year, Semester, and Type  
- 📋 **View & Filter** — Filter students by gender, category, year, semester, course, or type (Hosteller / Day Scholar)  
- 🔎 **Search** — Look up students instantly by *Student ID* or *Roll No*  
- ✏️ **Update Records** — Modify student details with inline editable forms  
- 🗑️ **Delete Students** — Secure deletion with confirmation checkbox  
- 🏨 **Hosteller / Day Scholar Support** — Hostel info (Room, Building, Block) and Bus info (Bus No, Route) managed dynamically  
- 📂 **Export to CSV** — Download filtered data instantly  
- ⚡ **Lightweight & Fast** — Runs locally with SQLite, no heavy setup required  

---

## 🛠️ Tech Stack  

- **Frontend / UI**: [Streamlit](https://streamlit.io/) 🎨  
- **Backend**: Python 🐍  
- **Database**: SQLite (lightweight file-based DB) 🗄️  
- **Libraries**: Pandas, IO, sqlite3  

---

## 📂 Project Structure  

EduTrack/
│── app.py # Main Streamlit UI (CRUD + Filters + Export)
│── backend.py # Database functions (CRUD operations, filters)
│── students.db # SQLite database (auto-created)
│── assets/ # Place screenshots / demo GIFs here
│── README.md # Documentation

