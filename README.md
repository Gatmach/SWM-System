# SWM-System
# ♻️ Smart Waste Management System (SWMS)

> A smart city web application that supports real-time monitoring and optimization of waste collection using IoT and data analytics.

`SWMS` is a Django-based web system that enhances municipal waste collection through intelligent bin tracking, route optimization, and administrative oversight. Designed for urban settings, the system reduces overflow issues, optimizes collection routes, and improves public hygiene by integrating smart bin sensors, a responsive dashboard, and a secure user interface.

---

## 🌟 Features

- 🗑️ **Smart Bin Monitoring**  
  Tracks bin status (full, empty, needs attention) in real time.

- 🧠 **Data-Driven Insights**  
  Analyze waste collection patterns and trends via interactive dashboards.

- 🧭 **Route Optimization (Planned)**  
  Optimize waste truck paths to save time and fuel.

- 🔐 **User Authentication**  
  Secure login system with role-based access for Admins and Field Officers.

- 📱 **Responsive Web Interface**  
  Works across desktops, tablets, and smartphones.

---

## ⚙️ Tech Stack

| Layer        | Technology                        |
|--------------|------------------------------------|
| Frontend     | HTML, CSS, JavaScript              |
| Backend      | Django (Python)                    |
| Database     | PostgreSQL                         |
| Visualization| Chart.js, Django Templates         |
| Environment  | Python `venv` (located in `smartBin/`) |
| Deployment   | GitHub, Railway/Render (Optional)  |

---

### **Getting Started**

#### **1. Clone the Repository**

### **2. Create and Activate Virtual Environment
     python -m venv virtualenv_name
    virtualenv_name\Scripts\activate         # For Windows
    source virtualenv_name/bin/activate   # For Linux/macOS
### **3.  Install Requirements
    pip install -r requirements.txt
### **4. Configure PostgreSQL Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    Then run:
    python manage.py makemigrations
    python manage.py migrate
### **5.  Run the Application
    python manage.py runserver

