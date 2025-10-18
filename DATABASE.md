
## 🧩 Health Synx – Database Structure

### 🔹 1. **User Model (Custom)**

**Table:** `users_user`

| Field                     | Type                          | Notes                               |
| ------------------------- | ----------------------------- | ----------------------------------- |
| id                        | AutoField (PK)                | Primary Key                         |
| username                  | CharField (unique)            | Auto-generated if not set           |
| first_name                | CharField                     |                                     |
| last_name                 | CharField                     |                                     |
| email                     | EmailField                    | Can be unique if you choose         |
| phone_number              | CharField                     | Optional                            |
| gender                    | CharField                     | (‘male’, ‘female’)                  |
| role                      | CharField                     | Choices: Admin, Doctor, Nurse, etc. |
| department_id             | FK → `departments_department` | Nullable                            |
| patient_type              | CharField                     | (‘inpatient’, ‘outpatient’)         |
| password                  | CharField                     | Hashed password                     |
| is_active, is_staff, etc. | Boolean                       | Inherited from `AbstractUser`       |

🧠 **Used by**: all other modules as a reference user object.

---

### 🔹 2. **Department**

**Table:** `departments_department`

| Field       | Type           | Notes              |
| ----------- | -------------- | ------------------ |
| id          | AutoField (PK) |                    |
| name        | CharField      | e.g., “Cardiology” |
| description | TextField      | Optional           |

🧠 **Used by**: doctors, nurses, and admin users to group by department.

---

### 🔹 3. **DoctorProfile**

**Table:** `doctors_doctorprofile`

| Field               | Type                    | Notes              |
| ------------------- | ----------------------- | ------------------ |
| id                  | AutoField (PK)          |                    |
| user_id             | OneToOne → `users_user` | Doctor’s account   |
| specialization      | CharField               | e.g., “Pediatrics” |
| license_number      | CharField               |                    |
| years_of_experience | IntegerField            |                    |

🧠 **Used by**: `PatientProfile.assigned_doctor` and `DoctorQueue.doctor`.

---

### 🔹 4. **PatientProfile**

**Table:** `patients_patientprofile`

| Field              | Type                         | Notes             |
| ------------------ | ---------------------------- | ----------------- |
| id                 | AutoField (PK)               |                   |
| user_id            | OneToOne → `users_user`      | Patient’s account |
| dob                | DateField                    | Date of Birth     |
| assigned_doctor_id | FK → `doctors_doctorprofile` | Nullable          |

🧠 **Used by**: nurses, doctors, and billing workflows.

---

### 🔹 5. **PatientVitals**

**Table:** `patients_patientvitals`

| Field       | Type                                          | Notes                      |
| ----------- | --------------------------------------------- | -------------------------- |
| id          | AutoField (PK)                                |                            |
| patient_id  | FK → `users_user`                             | Must have `role='patient'` |
| temperature | DecimalField (max_digits=4, decimal_places=1) | Example: 37.2              |
| pulse_rate  | PositiveIntegerField                          | BPM                        |
| recorded_at | DateTimeField (auto_now_add=True)             |                            |

🧠 **Used by**: `DoctorQueue` (links vitals to queue).

---

### 🔹 6. **DoctorQueue**

**Table:** `patients_doctorqueue`

| Field      | Type                              | Notes                                        |
| ---------- | --------------------------------- | -------------------------------------------- |
| id         | AutoField (PK)                    |                                              |
| patient_id | FK → `users_user`                 | Patient being queued                         |
| vitals_id  | FK → `patients_patientvitals`     | Latest vitals                                |
| doctor_id  | FK → `users_user`                 | Doctor assigned (nullable)                   |
| status     | CharField                         | waiting, with_doctor, sent_to_lab, completed |
| created_at | DateTimeField (auto_now_add=True) |                                              |
| updated_at | DateTimeField (auto_now=True)     |                                              |

🧠 **Used by**: doctor workflows and billing creation.

---

### 🔹 7. **DoctorNote**

**Table:** `patients_doctornote`

| Field         | Type                              | Notes |
| ------------- | --------------------------------- | ----- |
| id            | AutoField (PK)                    |       |
| patient_id    | FK → `users_user`                 |       |
| doctor_id     | FK → `users_user`                 |       |
| queue_item_id | FK → `patients_doctorqueue`       |       |
| diagnosis     | TextField                         |       |
| prescription  | TextField                         |       |
| created_at    | DateTimeField (auto_now_add=True) |       |

🧠 **Used by**: doctors to log patient notes per consultation.

---

### 🔹 8. **BillingRecord**

**Table:** `billing_billingrecord`

| Field           | Type                              | Notes                  |
| --------------- | --------------------------------- | ---------------------- |
| id              | AutoField (PK)                    |                        |
| patient_id      | FK → `users_user`                 | Patient being billed   |
| doctor_queue_id | FK → `patients_doctorqueue`       | Source of consultation |
| amount          | DecimalField                      | e.g., 1500.00          |
| description     | CharField                         | “Consultation Fee”     |
| created_at      | DateTimeField (auto_now_add=True) |                        |

🧠 **Used by**: Billing Officers and reports.

---

## 🔗 Relationships Summary (ERD Overview)

```
User (role='patient') ───< PatientProfile
User (role='doctor')  ───< DoctorProfile

PatientProfile ──(optional)──> DoctorProfile (assigned_doctor)
PatientVitals ───< DoctorQueue ───< DoctorNote ───> Doctor (User)
DoctorQueue ───< BillingRecord

User (role='nurse') interacts with PatientVitals & DoctorQueue.
```

---

## 🧠 Example Data Flow

1. **Admin / Hospital Admin** adds a new patient → a new `User` + `PatientProfile`.
2. **Nurse** records vitals → `PatientVitals` created → patient added to `DoctorQueue`.
3. **Doctor** opens queue, writes a note → `DoctorNote` saved.
4. When consultation ends → `DoctorQueue.mark_completed()` triggers → new `BillingRecord` created.

---
