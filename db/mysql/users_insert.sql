-- ======================================================
-- Users insert for health_db.users_user
-- ======================================================

-- Doctors
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'lilyjohns', 'Lily', 'Johns', 'lilyjohns@example.com', 0, 1, NOW(), '0710000001', 'doctor', 'male', NULL, 3),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'paulajohns', 'Paula', 'Johns', 'pauljohns@example.com', 0, 1, NOW(), '0710000002', 'doctor', 'female', NULL, 3);

-- Pharmacists
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'janemikes', 'Jane', 'Mikes', 'janemikes@example.com', 0, 1, NOW(), '0720000001', 'pharmacist', 'female', NULL, 2),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'karengitau', 'Karen', 'Gitau', 'karengitau@example.com', 0, 1, NOW(), '0720000002', 'pharmacist', 'female', NULL, 2);

-- Lab Technicians
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'robertmakau', 'Robert', 'Makau', 'robertmakau@example.com', 0, 1, NOW(), '0730000001', 'lab_tech', 'male', NULL, 6),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'robinmaina', 'Robin', 'Maina', 'robinmaina@example.com', 0, 1, NOW(), '0730000002', 'lab_tech', 'male', NULL, 6);

-- Imaging Technicians
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'allankizito', 'Allan', 'Kizito', 'allankizito@example.com', 0, 1, NOW(), '0740000001', 'imaging_tech', 'male', NULL, 7),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'berylkanini', 'Beryl', 'Kanini', 'berylkanini@example.com', 0, 1, NOW(), '0740000002', 'imaging_tech', 'female', NULL, 7);

-- Billing Officers
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'marykanes', 'Mary', 'Kanes', 'marykanes@example.com', 0, 1, NOW(), '0750000001', 'billing', 'female', NULL, 1),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'nancybrowns', 'Nancy', 'Browns', 'nancybrowns@example.com', 0, 1, NOW(), '0750000002', 'billing', 'female', NULL, 1);

-- Nurses
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'kellypeters', 'Kelly', 'Peters', 'kellypeters@example.com', 0, 1, NOW(), '0760000001', 'nurse', 'female', NULL, 4),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'hopelagat', 'Hope', 'Lagat', 'hopelagat@example.com', 0, 1, NOW(), '0760000002', 'nurse', 'female', NULL, 4);

-- Hospital Admins
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'susanpeters', 'Susan', 'Peters', 'susanpeters@example.com', 0, 1, NOW(), '0770000001', 'hospital_admin', 'female', NULL, 5),
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 0, 'wesleywafula', 'Wesley', 'Wafula', 'wesleywafula@example.com', 0, 1, NOW(), '0770000002', 'hospital_admin', 'male', NULL, 5);

-- Admins (superusers)
INSERT INTO users_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone_number, role, gender, patient_type, department_id)
VALUES
('bcrypt_sha256\$2b\$12\$QiWL4/hI4KsOtY4h217TFOqZ3czfEQn0JjTzNh8e.0gz3wIsnKqXK'
, NOW(), 1, 'admin1', 'Admin', 'One', 'admin1@example.com', 1, 1, NOW(), '0700000001', 'admin', 'male', NULL, 5);

