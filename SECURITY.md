# 🔐 Security Overview for Health Synx

The **Health Synx Hospital Management System** is designed with multiple layers of security to protect sensitive patient and hospital data. Below is a detailed summary of how the system enforces security across authentication, data protection, and deployment.

---

## 🧱 1. Authentication & Authorization

**Custom User Model**

* Extends Django's `AbstractUser` with fields for `role`, `department`, and `patient_type`.
* Supports multiple user types (Admin, Doctor, Nurse, etc.) with granular access control.

**Role-Based Access Control (RBAC)**

* Views are restricted by role using a custom decorator `@role_required(['doctor', 'nurse', ...])`.
* Prevents unauthorized access to specific modules or data.

**Secure Password Handling**

* Uses Django's built-in password hashing (PBKDF2).
* Enforces strong password rules using validators.
* Supports password reset and change via Django's auth system.

---

## 🧰 2. Data Protection & Privacy

**Sensitive Data Access**

* Only authorized roles can access patient details, billing info, or diagnoses.
* Department-based filtering ensures staff only access relevant patient data.

**SQL Injection Prevention**

* Django ORM automatically escapes queries, protecting from SQL injection.

---

## 🧰 3. Input Validation & CSRF Protection

* All POST forms use Django's built-in CSRF token (`{% csrf_token %}`).
* Form validation ensures only clean and valid data is saved.
* Unique username generation prevents duplicate or invalid entries.

---


## 🧰 4. Password & Account Security

**Password Validators**

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

* Enforces minimum password length and complexity.
* Prevents reuse of weak or common passwords.

---


## 🧰 5. Deployment Security

  ```
* Store secrets in environment variables:

  ```python
  SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
  DATABASES['default']['PASSWORD'] = os.getenv('DB_PASSWORD')
  ```

---

## 🧰 6. Future API Security (for Django REST Framework)

When integrating DRF:

* Use JWT or Token Authentication.
* Apply permission classes per role.
* Add throttling/rate limiting with `django-ratelimit`.

---

## ✅ Summary of Security Layers

| Layer                    | Protection Method                      |
| ------------------------ | -------------------------------------- |
| Authentication           | Django Auth + Custom Roles             |
| Authorization            | Role-based decorators                  |
| Data Encryption          | HTTPS + Hashed passwords               |
| Input Validation         | Django Forms + CSRF                    |
| SQL Injection Prevention | ORM (safe queries)                     |
| Session Protection       | Secure & HttpOnly Cookies              |
| Error Handling           | Custom error pages + Logging           |
| Deployment Safety        | Env vars + DEBUG=False + Allowed Hosts |

---

## 🛡️ Security Best Practices Checklist

* [ ] Rotate `SECRET_KEY` and DB credentials periodically
* [ ] Enforce password complexity
* [ ] Disable `DEBUG` on production
* [ ] Apply role-based restrictions on all views
* [ ] Regularly back up the database securely
* [ ] Use environment variables for sensitive configs
* [ ] Log and monitor all login attempts (future)
