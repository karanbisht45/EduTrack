# 🎓 InsightED AI

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-ff4b4b?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Database-SQLite-green?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/AI-Cohere-purple" alt="Cohere">
</p>

---

## 🌟 Overview  

> ⚡ **InsightED AI** is a next-gen **Student Database Management System (DBMS)** powered by **AI + Streamlit**.  
It provides a **fast, lightweight, and intelligent interface** for managing student records — featuring **CRUD operations**, **filters**, **search**, **AI-powered SQL queries**, **performance prediction**, and **hosteller/day-scholar support**, all built on an **SQLite database**.

---

## ✨ Features  

💡 **What you can do with InsightED AI:** 

- ➕ **Add Students** — Save student details including ID, Roll No, Name, Course, Address, Year, Semester, Type, and transport/hostel info.  
- 📋 **View & Filter** — Filter records by **gender, category, year, semester, course, or type**.  
- 🔎 **Search** — Instantly find students by **Student ID** or **Roll No**.  
- ✏️ **Update Records** — Edit student details with inline forms.  
- 🗑️ **Delete Students** — Remove records safely with confirmation.  
- 🏨 **Hosteller / Day Scholar Support** — Manage **hostel info** (Room, Building, Block) or **bus info** (Bus No, Route).  
- 🤖 **AI Database Assistant** — Convert natural language into **safe SQL SELECT queries** using **Cohere**.
- 📈 **AI Performance Predictor** — Predicts and analyzes student performance trends using ML models. 
- 📂 **Export to CSV** — Download filtered student data instantly.  
- 🔐 **User Authentication** — Secure login/signup with **SHA256 hashed passwords**.  
- ⚡ **Lightweight & Fast** — Runs locally with **zero heavy setup**.  

---

## 🛠️ Tech Stack  

| Layer        | Technology |
|--------------|------------|
| 🎨 **Frontend** | [Streamlit](https://streamlit.io/) |
| 🐍 **Backend** | Python |
| 🗄️ **Database** | SQLite |
| 🤖 **AI Integration** | Cohere API |
| 📦 **Libraries** | Pandas, sqlite3, hashlib, io |

---

## 📂 Project Structure  
```bash
EduTrack/
├── app.py # 🎨 Main Streamlit UI (CRUD + Filters + AI Assistant + Export)
├── backend.py # ⚙️ Database functions (CRUD, filters, AI query execution)
├── auth.py # 🔑 User authentication (signup/login)
├── students.db # 🗄️ SQLite database (auto-created)
└── README.md # 📘 Project documentation
```
---

## 🚀 Getting Started  

1. **Clone the repository**
```bash
git clone https://github.com/karanbisht45/InsightED-AI.git
cd InsightED-AI
```

2. **Install dependencies**
```bash
pip install streamlit pandas cohere
```

3. **Set your Cohere API Key**
```bash
Replace YOUR_COHERE_API_KEY in app.py or backend.py with your key.
```

4. **Run the app**
```bash
streamlit run app.py
```
---

## 💡 AI Assistant Examples
You can ask queries like:

-🏨 "Show all hostellers in 2nd year"

-🎓 "List students taking B.Tech CSE in semester 4"

---

## 📝 Notes
```bash
✔️ Only SELECT queries are allowed via the AI assistant (for safety).
✔️ Passwords are securely hashed with SHA256.
✔️ CSV export respects applied filters.
```
