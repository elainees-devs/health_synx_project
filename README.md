# 🏥 Health Synx – Hospital Management System (API Version)

**Health Synx** is a modular **Hospital Management API** built with **Django REST Framework**.  
It simplifies patient registration, vitals tracking, doctor queue management, and billing workflows in a hospital setting.

---

## 📘 Documentation

All API endpoints and models are documented automatically using **Swagger** and **ReDoc**:

- **Swagger UI** → [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc UI** → [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
- **OpenAPI Schema (JSON)** → [http://127.0.0.1:8000/swagger.json](http://127.0.0.1:8000/swagger.json)

For advanced references:
- [**Database Structure**](./DATABASE.md)
- [**Security Overview**](./SECURITY.md)

---

## 🚀 Features

### 👩‍⚕️ Core Modules

#### **Users & Roles**
Supports multiple user types with permission-based access:
- Admin
- Hospital Admin
- Doctor
- Nurse
- Lab Technician
- Pharmacist
- Billing Officer
- Patient

#### **Patient Management**
- Register and manage patients.
- Automatic username generation.
- View and edit patient records.

#### **Vitals Recording**
- Nurses can record temperature, pulse, etc.
- Historical vitals tracking per patient.

#### **Doctor Queue**
- Automatically queue patients after vitals recording.
- Status transitions: `waiting → with_doctor → lab/pharmacy → completed`.

#### **Doctor Notes**
- Doctors record diagnoses and prescriptions.
- Notes are linked to queue and patient visits.

#### **Billing**
- Billing records auto-generated after consultations.
- Integrated with doctor queue and prescriptions.

---

## 🧰 Tech Stack

| Component             | Technology                      |
| --------------------- | ------------------------------- |
| **Backend Framework** | Django 5.x + Django REST Framework |
| **Database**          | MySQL                           |
| **API Docs**          | drf-yasg (Swagger + ReDoc)      |
| **Authentication**    | Token-based Auth (DRF)          |
| **Language**          | Python 3.10+                    |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/health_synx.git
cd health_synx
````

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database (MySQL)

Update `health_synx/settings.py`:

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

Then migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Server (HTTP)

```bash
python manage.py runserver
```

Visit:
👉 [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 🧩 App Structure

```
health_synx/
│
├── users/             # Authentication & roles
├── patients/          # Patient, vitals, queue, prescriptions
├── doctors/           # Doctor profiles and notes
├── nurses/            # Nurse-related endpoints
├── billing/           # Billing logic
├── departments/       # Hospital departments
├── diagnostics/       # Lab and diagnostic tests
├── pharmacy/          # Pharmacy & medicines
│
├── manage.py
└── README.md
```

---

## 🧑‍💻 Roles & Access Control

| Role               | Permissions                     |
| ------------------ | ------------------------------- |
| **Admin**          | Full access                     |
| **Hospital Admin** | Manage staff & patients         |
| **Nurse**          | Record vitals, manage queue     |
| **Doctor**         | View patients, record diagnosis |
| **Billing**        | Manage payments                 |
| **Patient**        | Limited self-access             |

---

## 🔑 Authentication

All endpoints use **Token Authentication**.

### Obtain Token

```bash
POST /api/login/
```

Response:

```json
{
  "token": "your_auth_token"
}
```

Include in headers:

```
Authorization: Token your_auth_token
```

---

## 🧪 Example Test Users

| Username    | Role            | Password     |
| ----------- | --------------- | ------------ |
| susanpeters | Hospital Admin  | Nairobi2025@ |
| kellypeters | Nurse           | Nairobi2025  |
| lilyjohns   | Doctor          | Nairobi2025  |
| marykanes   | Billing Officer | Nairobi2025  |

---

## 🛡️ Error Handling

| Error Type | Description             |
| ---------- | ----------------------- |
| **400**    | Invalid input data      |
| **401**    | Authentication required |
| **403**    | Permission denied       |
| **404**    | Resource not found      |
| **500**    | Server-side issue       |

---

## 🧱 Future Enhancements

* ✅ Appointment scheduling system
* ✅ Laboratory integration
* ✅ Pharmacy inventory management
* ✅ Mobile app (React Native)
* ✅ Cloud deployment (AWS / Docker)

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/new-module`)
3. Commit and push your changes
4. Submit a Pull Request

---

## 👩‍💻 Author

**System Developed by:**
*Elaine Muhombe*
💼 Backend Developer | DevOps Learner
📧 [support@healthsynx.com](mailto:support@healthsynx.com)

```
