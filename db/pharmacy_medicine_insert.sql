-- ======================================================
-- Medicines insert for health_db.pharmacy_medicine
-- ======================================================

INSERT INTO pharmacy_medicine
(name, description, stock, price, expiry_date, created_at, updated_at, supplier_id, form, type)
VALUES
-- Supplier 1: Medicare Supplies Ltd
('Paracetamol 500mg', 'Pain reliever and fever reducer.', 100, 50.00, '2026-12-31', NOW(), NOW(), 1, 'Tablet', 'Analgesic'),
('Amoxicillin 250mg', 'Antibiotic for bacterial infections.', 80, 120.00, '2025-11-30', NOW(), NOW(), 1, 'Capsule', 'Antibiotic'),
('Cough Syrup', 'Relieves cough and throat irritation.', 50, 150.00, '2025-10-31', NOW(), NOW(), 1, 'Syrup', 'Cough Suppressant'),

-- Supplier 2: HealthPlus Pharma
('Ibuprofen 200mg', 'Anti-inflammatory and pain reliever.', 90, 70.00, '2026-01-15', NOW(), NOW(), 2, 'Tablet', 'Analgesic'),
('Azithromycin 250mg', 'Antibiotic for respiratory infections.', 60, 200.00, '2025-09-30', NOW(), NOW(), 2, 'Tablet', 'Antibiotic'),
('Vitamin C 500mg', 'Supports immune system.', 120, 40.00, '2027-06-30', NOW(), NOW(), 2, 'Tablet', 'Supplement'),

-- Supplier 3: PharmaCare Ltd
('Metformin 500mg', 'Used to treat type 2 diabetes.', 70, 90.00, '2026-03-31', NOW(), NOW(), 3, 'Tablet', 'Antidiabetic'),
('Loratadine 10mg', 'Allergy relief.', 100, 60.00, '2026-05-31', NOW(), NOW(), 3, 'Tablet', 'Antihistamine'),
('Omeprazole 20mg', 'Reduces stomach acid.', 80, 150.00, '2026-07-31', NOW(), NOW(), 3, 'Capsule', 'Antacid'),

-- Supplier 4: Wellness Pharma
('Aspirin 75mg', 'Blood thinner and pain reliever.', 60, 50.00, '2026-02-28', NOW(), NOW(), 4, 'Tablet', 'Analgesic'),
('Doxycycline 100mg', 'Antibiotic for various infections.', 90, 180.00, '2025-12-31', NOW(), NOW(), 4, 'Capsule', 'Antibiotic'),
('Salbutamol Inhaler', 'Relieves asthma symptoms.', 30, 500.00, '2025-11-30', NOW(), NOW(), 4, 'Inhaler', 'Bronchodilator'),

-- Supplier 5: Global Meds
('Cetirizine 10mg', 'Allergy relief.', 100, 70.00, '2026-06-30', NOW(), NOW(), 5, 'Tablet', 'Antihistamine'),
('Amoxicillin-Clavulanate', 'Broad-spectrum antibiotic.', 50, 250.00, '2026-01-31', NOW(), NOW(), 5, 'Tablet', 'Antibiotic'),
('Paracetamol Syrup', 'Fever and pain reducer for children.', 40, 120.00, '2025-10-31', NOW(), NOW(), 5, 'Syrup', 'Analgesic'),

-- Supplier 6: QuickPharma Supplies
('Furosemide 40mg', 'Diuretic for edema and hypertension.', 60, 90.00, '2026-03-31', NOW(), NOW(), 6, 'Tablet', 'Diuretic'),
('Ceftriaxone 1g', 'Antibiotic injection for serious infections.', 20, 500.00, '2025-12-31', NOW(), NOW(), 6, 'Injection', 'Antibiotic'),
('Prednisone 10mg', 'Steroid for inflammation.', 50, 150.00, '2026-05-31', NOW(), NOW(), 6, 'Tablet', 'Corticosteroid'),

-- Supplier 7: SafeMeds Ltd
('Amlodipine 5mg', 'Treatment for hypertension.', 80, 100.00, '2026-04-30', NOW(), NOW(), 7, 'Tablet', 'Antihypertensive'),
('Clarithromycin 500mg', 'Antibiotic for respiratory infections.', 60, 200.00, '2026-02-28', NOW(), NOW(), 7, 'Tablet', 'Antibiotic'),
('Omeprazole Suspension', 'Stomach acid reducer for children.', 30, 180.00, '2025-12-31', NOW(), NOW(), 7, 'Syrup', 'Antacid'),

-- Supplier 8: CityHealth Suppliers
('Simvastatin 20mg', 'Cholesterol-lowering drug.', 70, 120.00, '2026-08-31', NOW(), NOW(), 8, 'Tablet', 'Lipid-Lowering'),
('Cefuroxime 250mg', 'Antibiotic for bacterial infections.', 80, 150.00, '2026-06-30', NOW(), NOW(), 8, 'Tablet', 'Antibiotic'),
('Ibuprofen Suspension', 'Pain relief for children.', 50, 90.00, '2026-03-31', NOW(), NOW(), 8, 'Syrup', 'Analgesic'),

-- Supplier 9: Prime Pharma Ltd
('Losartan 50mg', 'Hypertension treatment.', 60, 110.00, '2026-09-30', NOW(), NOW(), 9, 'Tablet', 'Antihypertensive'),
('Azithromycin Syrup', 'Antibiotic for children.', 40, 200.00, '2025-11-30', NOW(), NOW(), 9, 'Syrup', 'Antibiotic'),
('Metronidazole 400mg', 'Treatment for infections.', 90, 80.00, '2026-01-31', NOW(), NOW(), 9, 'Tablet', 'Antibiotic'),

-- Supplier 10: Trust Meds
('Hydrochlorothiazide 25mg', 'Diuretic for hypertension.', 70, 90.00, '2026-04-30', NOW(), NOW(), 10, 'Tablet', 'Diuretic'),
('Ciprofloxacin 500mg', 'Broad-spectrum antibiotic.', 60, 150.00, '2026-03-31', NOW(), NOW(), 10, 'Tablet', 'Antibiotic'),
('Vitamin D 1000IU', 'Supports bone health.', 100, 50.00, '2027-05-31', NOW(), NOW(), 10, 'Tablet', 'Supplement'),

-- Supplier 11: Reliable Pharma
('Enalapril 10mg', 'ACE inhibitor for hypertension.', 60, 100.00, '2026-06-30', NOW(), NOW(), 11, 'Tablet', 'Antihypertensive'),
('Clindamycin 300mg', 'Antibiotic for infections.', 50, 180.00, '2026-01-31', NOW(), NOW(), 11, 'Capsule', 'Antibiotic'),
('Paracetamol 250mg', 'Pain and fever relief for children.', 90, 40.00, '2025-12-31', NOW(), NOW(), 11, 'Tablet', 'Analgesic'),

-- Supplier 12: EastPharma Ltd
('Prednisolone 5mg', 'Steroid for inflammation.', 40, 120.00, '2026-03-31', NOW(), NOW(), 12, 'Tablet', 'Corticosteroid'),
('Amoxicillin 500mg', 'Broad-spectrum antibiotic.', 80, 150.00, '2026-04-30', NOW(), NOW(), 12, 'Capsule', 'Antibiotic'),
('Cough Syrup Advanced', 'Relieves cough and cold symptoms.', 30, 200.00, '2025-11-30', NOW(), NOW(), 12, 'Syrup', 'Cough Suppressant'),

-- Supplier 13: HealthLine Supplies
('Levothyroxine 50mcg', 'Treatment for hypothyroidism.', 60, 150.00, '2026-07-31', NOW(), NOW(), 13, 'Tablet', 'Hormone'),
('Erythromycin 250mg', 'Antibiotic for infections.', 50, 200.00, '2026-05-31', NOW(), NOW(), 13, 'Tablet', 'Antibiotic'),
('Paracetamol Extra', 'Strong pain relief.', 100, 70.00, '2026-06-30', NOW(), NOW(), 13, 'Tablet', 'Analgesic'),

-- Supplier 14: MedLink Ltd
('Atorvastatin 10mg', 'Cholesterol-lowering medication.', 80, 150.00, '2026-08-31', NOW(), NOW(), 14, 'Tablet', 'Lipid-Lowering'),
('Metformin XR 500mg', 'Diabetes management.', 70, 120.00, '2026-09-30', NOW(), NOW(), 14, 'Tablet', 'Antidiabetic'),
('Omeprazole 40mg', 'Reduces stomach acid.', 60, 180.00, '2026-10-31', NOW(), NOW(), 14, 'Capsule', 'Antacid'),

-- Supplier 15: CareMeds Ltd
('Simvastatin 40mg', 'Cholesterol-lowering medication.', 50, 180.00, '2026-12-31', NOW(), NOW(), 15, 'Tablet', 'Lipid-Lowering'),
('Clopidogrel 75mg', 'Blood thinner.', 40, 200.00, '2026-11-30', NOW(), NOW(), 15, 'Tablet', 'Antiplatelet'),
('Amoxicillin 125mg Syrup', 'Antibiotic for children.', 60, 150.00, '2025-10-31', NOW(), NOW(), 15, 'Syrup', 'Antibiotic');
