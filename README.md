# 🎓 EduTrack — Student Database Management System (DBMS)

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-ff4b4b?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Database-SQLite-green?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/AI-Cohere-purple" alt="Cohere">
</p>

---

## 🌟 Overview  

EduTrack is a **Student Database Management System (DBMS)** built with **Python + Streamlit**.  
It provides a **fast, lightweight, and intuitive interface** for managing student records — including **CRUD operations**, **filters**, **search**, **AI-assisted queries**, and **hosteller/day-scholar support** — all backed by an **SQLite database**.

---

## ✨ Features  

- ➕ **Add Students** — Add full student details including ID, Roll No, Name, Course, Address, Year, Semester, Type, and transport/hostel info.  
- 📋 **View & Filter** — Filter students by **gender, category, year, semester, course, or type**.  
- 🔎 **Search** — Lookup students instantly by **Student ID** or **Roll No**.  
- ✏️ **Update Records** — Edit student details directly in inline forms.  
- 🗑️ **Delete Students** — Safe deletion with a confirmation checkbox.  
- 🏨 **Hosteller / Day Scholar Support** — Manage **hostel info** (Room, Building, Block) and **bus info** (Bus No, Route) dynamically.  
- 🤖 **AI Database Assistant** — Natural language queries converted to **safe SQL SELECT queries** via **Cohere**.  
- 📂 **Export to CSV** — Download filtered student data instantly.  
- 🔐 **User Authentication** — Signup/Login system with **hashed passwords (SHA256)**.  
- ⚡ **Lightweight & Fast** — Runs locally, no heavy setup required.  

---

## 🛠️ Tech Stack  

- **Frontend / UI:** [Streamlit](https://streamlit.io/) 🎨  
- **Backend:** Python 🐍  
- **Database:** SQLite 🗄️  
- **AI Integration:** Cohere API 🤖  
- **Libraries:** Pandas, sqlite3, hashlib, io  

---

## 📂 Project Structure  

EduTrack/
│── app.py # Main Streamlit UI (CRUD + Filters + AI Assistant + Export)
│── backend.py # Database functions (CRUD, filters, AI query execution)
│── auth.py # User authentication (signup/login)
│── students.db # SQLite database (auto-created)
│── assets/ # Screenshots, demo GIFs, or additional assets
│── README.md # Project documentation

---


---

## 🚀 Getting Started  

1. **Clone the repository**
```bash
git clone https://github.com/karanbisht45/EduTrack.git
cd EduTrack
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
