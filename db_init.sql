CREATE DATABASE hospital_db;
USE hospital_db;
--command to execute the whole file a once SOURCE path to you sql file
--mysql -u root -p hospital_db < your_file.sql 

-- Patients Table
CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    address TEXT,
    phone VARCHAR(15),
    disease VARCHAR(255)
);

-- Doctors Table
CREATE TABLE Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100)
);

-- Appointments Table (Fixed Version)
CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    status VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);

-- Billing Table
CREATE TABLE Billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    status ENUM('Paid', 'Unpaid'),
    payment_method ENUM('Cash', 'Card', 'Insurance'),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- Pharmacy Table
CREATE TABLE Pharmacy (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    stock INT,
    price DECIMAL(10,2)
);

-- Staff Table
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role ENUM('Nurse', 'Receptionist', 'Lab Technician'),
    phone VARCHAR(15),
    salary DECIMAL(10,2)
);
