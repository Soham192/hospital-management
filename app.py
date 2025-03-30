from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection (Using auth_socket)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        unix_socket="/var/run/mysqld/mysqld.sock",  # Update this if necessary
        database="hospital_db"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

@app.route('/')
def home():
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    disease = request.form['disease']

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

    cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status) VALUES (%s, %s, %s, %s)",
                   (patient_id, doctor_id, appointment_date, status))
    db.commit()
    return redirect('/')

# Payment
@app.route('/add_payment', methods=['POST'])
def add_payment():
    patient_id = request.form['patient_id']
    amount = request.form['amount']
    status = request.form['status']
    payment_method = request.form['payment_method']

    cursor.execute("INSERT INTO Billing (patient_id, amount, status, payment_method) VALUES (%s, %s, %s, %s)",
                   (patient_id, amount, status, payment_method))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
