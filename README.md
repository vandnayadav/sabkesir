# online_learning_website

# 📚 Sabke Sir - Online Learning Platform

Sabke Sir is an online learning platform where students can explore courses, sign up/login, and start their learning journey easily.

---

## 🚀 Features

- 👤 User Authentication (Signup / Login / Logout)
- 🔐 Forgot Password (Email Reset Link)
- 🧑‍💻 Admin Panel (Django Admin)
- 📚 Course Display
- 🎨 Responsive UI (HTML, CSS, JavaScript)
- ⚡ Simple and Fast Interface

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Email Service:** SMTP (Gmail)

---

## 📂 Project Structure
learning_platform/
│── app/
│ ├── views.py
│ ├── models.py
│ ├── urls.py
│
│── templates/
│── static/
│── db.sqlite3
│── manage.py


### 1️⃣ Clone Repository


git clone https://github.com/your-username/sabkesir.git

cd sabkesir


---

### 2️⃣ Create Virtual Environment


python -m venv venv
venv\Scripts\activate


---

### 3️⃣ Install Dependencies


pip install -r requirements.txt


---

### 4️⃣ Run Migrations


python manage.py makemigrations
python manage.py migrate


---

### 5️⃣ Run Server


python manage.py runserver


Open in browser:


http://127.0.0.1:8000/


---

## 🔑 Email Configuration (Important)

For forgot password functionality, configure Gmail SMTP:

