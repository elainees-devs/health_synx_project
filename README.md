# 🏥 Health Synx – Hospital Management System

**Health Synx** is a modular hospital management platform built with **Django**.
It simplifies patient registration, vital recording, doctor queue management, and billing operations in a hospital environment.

---

#### 📘 Documentation

For detailed project references, check out:

- [**Database Structure**](./DATABASE.md)
- [**Security Overview**](./SECURITY.md)


---

### 🚀 Features

#### 👩‍⚕️ Core Modules

* **Users & Roles** — Supports multiple user roles:

  * Admin, Hospital Admin, Doctor, Nurse, Lab Tech, Pharmacist, Billing Officer, and Patient.
* **Patient Management**

  * Register new patients with automatic username generation.
  * Edit or delete patient details.
  * View all registered patients.
* **Patient Vitals**

  * Nurses can record vitals (temperature, pulse rate, etc.).
  * Vitals history per patient.
* **Doctor Queue**

  * Automatically queue patients for doctor consultation after vitals recording.
  * Manage queue status: waiting → with doctor → lab/pharmacy → completed.
* **Doctor Notes**

  * Doctors can record diagnosis and prescriptions.
* **Billing**

  * Billing record automatically generated after consultation completion.

---

### 🧰 Tech Stack

| Component             | Technology                      |
| --------------------- | ------------------------------- |
| **Backend Framework** | Django 5.x                      |
| **Database**          | MySQL                           |
| **Frontend**          | HTML, Bootstrap / Tailwind      |
| **Authentication**    | Django Auth (Custom User Model) |
| **Language**          | Python 3.10+                    |

---

### ⚙️ Installation Guide

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/health_synx.git
cd health_synx
```

#### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Database (MySQL)

In your `health_synx/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'health_synx',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Then run:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

#### 5️⃣ Create Superuser

```bash
python3 manage.py createsuperuser
```

#### 6️⃣ Run the Development Server

```bash
python3 manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 🧩 App Structure

```
health_synx/
│
├── users/             # User & role management
├── patients/          # Patient registration, vitals, queue
├── doctors/           # Doctor profiles and notes
├── billing/           # Billing records
├── departments/       # Hospital departments
│
├── templates/         # Shared HTML templates
├── static/            # CSS, JS, images
│
├── manage.py
└── README.md
```

---

### 🧑‍💻 Roles & Access Control

| Role               | Permissions                     |
| ------------------ | ------------------------------- |
| **Admin**          | Full access                     |
| **Hospital Admin** | Manage staff & patients         |
| **Nurse**          | Record vitals, manage queue     |
| **Doctor**         | View patients, record diagnosis |
| **Billing**        | Process payments                |
| **Patient**        | Limited self-access             |

---

### 🧪 Example Test Users

| Username    | Role           | Password      |
| --------    | ------         | -----------   |
| susanpeters | Hosiptal Admin | `Nairobi2025@`|
| kellypeters | Nurse          | `Nairobi2025` |
| lilyjohns   | Doctor         | `Nairobi2025` |
| marykanes   | Billing Officer| `Nairobi2025` |

---

### 🛡️ Error Handling

Common issues:

* **IntegrityError (duplicate username)** — Automatically prevented using slug + random string.
* **Access Denied** — Controlled via `@role_required` decorator in `users.decorators`.

---

### 🧱 Future Enhancements

* ✅ Appointment scheduling system
* ✅ Laboratory results integration
* ✅ Pharmacy inventory tracking
* ✅ REST API using Django REST Framework
* ✅ React or Vue frontend

---

### 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/new-module`)
3. Commit changes
4. Open a Pull Request

---

### Author

System Developed by Elaine Muhombe

