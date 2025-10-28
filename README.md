
# 🏥 Health Synx – Hospital Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django&logoColor=white)  
![MySQL](https://img.shields.io/badge/MySQL-8-blue?logo=mysql&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative&logoColor=white)  

---

## 📌 Project Objective

**Health Synx** is a modular hospital management platform built with **Django**.  
It simplifies patient registration, vitals tracking, doctor queue management, billing operations, and notifications in a hospital environment.  
This repository documents the backend system and highlights role-based access control, dashboards, and API integration.

---

## 🚀 Overview

Health Synx is designed for hospital staff to manage patients, appointments, diagnostics, billing, pharmacy, and notifications efficiently.  

### Key Technologies

* **Python 3.10+** – Backend programming
* **Django 5.x** – Web framework
* **Django REST Framework (DRF)** – RESTful API development
* **MySQL** – Relational database
* **Swagger/OpenAPI** – API documentation

### Backend Concepts Implemented

* Role-Based Access Control (RBAC)
* Secure authentication/authorization
* Modular dashboards per role
* Efficient database queries using Django ORM
* API documentation with Swagger/OpenAPI

---
## ⚠️ Challenges Faced

During the development of **Health Synx**, several technical and operational challenges were encountered:

### 1️⃣ Role-Based Access Control (RBAC)
* Ensuring strict permissions for multiple roles (Admin, Doctor, Nurse, Billing Officer, Patient, etc.) was complex.
* Required custom decorators and DRF permission classes for API endpoints.
* Balancing flexibility and security without exposing sensitive patient data.

### 2️⃣ JWT Integration
* Implementing stateless authentication with JWT while maintaining session-like behavior for dashboards.
* Handling token refresh securely and ensuring proper expiration handling.

### 3️⃣ Database Design & Optimization
* Normalizing multiple related modules (patients, appointments, diagnostics, billing, pharmacy).
* Avoiding performance bottlenecks when querying large datasets (doctor queues, billing history).
* Using Django ORM efficiently with indexing and prefetching related objects.

### 4️⃣ Complex Workflows
* Automatic patient queue updates after vitals recording and doctor consultations.
* Coordinating multiple dashboards reflecting real-time data per role.
* Ensuring notifications and alerts were timely and accurate across modules.

### 5️⃣ Data Validation & Security
* Ensuring unique usernames and avoiding conflicts during patient registration.
* Securing sensitive data and endpoints with proper authentication and authorization.
* Preventing common attacks (SQL injection, CSRF, and improper access).

### 6️⃣ Testing & Maintainability
* Writing comprehensive unit tests for each app and API endpoint.
* Ensuring test data reflected realistic hospital operations.
* Maintaining modular, reusable code for scalability and future enhancements.

### 7️⃣ Integration Challenges
* Coordinating between modules like appointments, diagnostics, and billing to ensure consistent data flow.
* Preparing REST API endpoints with proper serialization, validation, and role-based access for external integrations.

---

Despite these challenges, **Health Synx** provides a robust, scalable, and secure backend system for hospital management, with clear separation of roles and responsibilities.


## 🏗 Project Structure

```

health_synx/
│
├── appointments/      # Manage patient appointments
├── billing/           # Billing records & invoices
├── departments/       # Hospital department management
├── diagnostics/       # Lab and diagnostic records
├── doctors/           # Doctor profiles and notes
├── health_synx/       # Main project settings
├── hospital_admins/   # Hospital admin-specific features
├── notifications/     # System notifications
├── nurses/            # Nurse modules: vitals, queues
├── patients/          # Patient registration and history
├── pharmacy/          # Pharmacy inventory and prescriptions
├── users/             # User & role management
│
├── manage.py
├── README.md
├── requirements.txt
├── SECURITY.md
└── venv/              # Virtual environment

````

---

## 🔑 Features

* **User & Role Management** – Admin, Hospital Admin, Doctor, Nurse, Pharmacist, Billing Officer, Patient
* **Patient Management** – Register, edit, delete, and view patients
* **Patient Vitals** – Nurses can record vitals and view history
* **Doctor Queue & Notes** – Automatic queuing and diagnosis recording
* **Appointments** – Schedule and track patient appointments
* **Billing System** – Automatic billing after consultations
* **Diagnostics** – Lab tests and results management
* **Pharmacy** – Inventory management and prescriptions
* **Notifications** – Alerts and reminders for staff and patients
* **REST API Endpoints** – Optional integration endpoints
* **Role-Based Dashboards** – Custom dashboard views for each role

---

## 🔑 Roles & Access Control

| Role               | Permissions                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| **Admin**          | Full access to all modules                                                   |
| **Hospital Admin** | Manage staff, patients, and departments                                     |
| **Doctor**         | View patients, record diagnosis, and manage doctor queue                     |
| **Nurse**          | Record patient vitals, manage patient queue                                  |
| **Billing Officer**| Process payments and manage billing records                                  |
| **Patient**        | Limited self-access to personal data and appointments                        |
| **Pharmacist**     | Manage pharmacy inventory and prescriptions                                  |
| **Lab Technician** | Record and manage lab test results                                           |
| **Imaging Technician** | Handle imaging test records and results                                  |

---
## ⚡ Installation

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
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure Database

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

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Running Tests

```bash
python manage.py test
```

Covers `users`, `patients`, `doctors`, `billing`, `appointments`, `pharmacy`, `nurses`, and `notifications`.

---

## 🔒 Security

* Role-based access via decorators and custom permissions
* Unique constraints prevent duplicate usernames
* Sensitive routes protected with Django Auth/JWT
* HTTPS recommended for production

See [SECURITY.md](./SECURITY.md) for details.

---

## 📤 Deployment

* **Deployment:** Backend API hosted with integrated Swagger docs in pythoneverywhere
* **Documentation** – Accessible at [https://elaines.pythonanywhere.com/swagger/](https://elaines.pythonanywhere.com/swagger/)

* **HTTPS Enforcement:** All production traffic redirected to HTTPS

## 🔑 Test Credentials (Development Only)

| Username    | Role                | Password       |
| ----------- | ---------------     | -------------- |
| susanpeters | Hospital Admin      | `TestPass123!` |
| kellypeters | Nurse               | `TestPass123!` |
| lilyjohns   | Doctor              | `TestPass123!` |
| marykanes   | Billing Officer     | `Test123Pass!` |
| janemikes   | Pharmacists         | `TestPass123!` |
| robertmakau | Lab Technician      | `TestPass123!` |
| allankizito | Imaging Technician  | `Test123Pass!` |

⚠️ Use for testing only; not for production.

---

## 🧱 Future Enhancements

Appointment scheduling notifications — notify patients and doctors via email or SMS

Laboratory results integration — allow lab technicians to upload and share test results digitally

Modern frontend with React or Vue — enhance user experience with a dynamic single-page interface

Complete REST API coverage — enable full external system integration and mobile app support

Containerization with Docker — simplify deployment and ensure consistent environments

---

## Author

The project was developed by Elaine Muhombe.

```

