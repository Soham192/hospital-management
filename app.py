from flask import Flask, render_template, request, redirect
import mysql.connector# sudo -E venv/bin/python3 app.py(-E is used due to )

app = Flask(__name__)

# MySQL Connection (Using auth_socket)
try:  
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        unix_socket="/var/run/mysqld/mysqld.sock",  # Update if necessary
        database="hospital_db"
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

@app.route('/')
def home():
    with db.cursor() as cursor:
        # Fetch Patients
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()

        # Fetch Doctors
        cursor.execute("SELECT * FROM Doctors")
        doctors = cursor.fetchall()

        # Fetch Appointments with correct table casing
        cursor.execute("""
            SELECT Appointments.appointment_id, Patients.name, Doctors.name, 
                   Appointments.appointment_date, Appointments.status
            FROM Appointments 
            JOIN Patients ON Appointments.patient_id = Patients.patient_id
            JOIN Doctors ON Appointments.doctor_id = Doctors.doctor_id
        """)
        appointments = cursor.fetchall()

    return render_template('index.html', patients=patients, doctors=doctors, appointments=appointments)

# Add Patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    disease = request.form['disease']

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)", 
                       (name, age, gender, disease))
        db.commit()
    return redirect('/')

# Add Doctor
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    specialty = request.form['specialty']
    phone = request.form['phone']
    email = request.form['email']

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Doctors (name, specialty, phone, email) VALUES (%s, %s, %s, %s)",
                       (name, specialty, phone, email))
        db.commit()
    return redirect('/')

# Schedule Appointment
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date = request.form['appointment_date']
    status = "Scheduled"

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status) VALUES (%s, %s, %s, %s)",
                       (patient_id, doctor_id, appointment_date, status))
        db.commit()
    return redirect('/')

# Add Payment
@app.route('/add_payment', methods=['POST'])
def add_payment():
    patient_id = request.form['patient_id']
    amount = request.form['amount']
    status = request.form['status']
    payment_method = request.form['payment_method']

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Billing (patient_id, amount, status, payment_method) VALUES (%s, %s, %s, %s)",
                       (patient_id, amount, status, payment_method))
        db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
