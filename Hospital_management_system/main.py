import sqlite3
from datetime import datetime

conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    admission_date TEXT,
    discharge_date TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS medical_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    diagnosis TEXT,
    prescription TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
)
''')

conn.commit()

def add_patient(name, age, gender):
    admission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO patients (name, age, gender, admission_date)
    VALUES (?, ?, ?, ?)
    ''', (name, age, gender, admission_date))
    conn.commit()

def discharge_patient(patient_id):
    discharge_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    UPDATE patients
    SET discharge_date = ?
    WHERE id = ?
    ''', (discharge_date, patient_id))
    conn.commit()

def add_medical_record(patient_id, diagnosis, prescription):
    cursor.execute('''
    INSERT INTO medical_records (patient_id, diagnosis, prescription)
    VALUES (?, ?, ?)
    ''', (patient_id, diagnosis, prescription))
    conn.commit()

def update_patient_info(patient_id, new_name, new_age, new_gender):
    cursor.execute('''
    UPDATE patients
    SET name = ?, age = ?, gender = ?
    WHERE id = ?
    ''', (new_name, new_age, new_gender, patient_id))
    conn.commit()

def search_patients(keyword):
    cursor.execute('''
    SELECT * FROM patients
    WHERE name LIKE ? OR id = ?
    ''', (f'%{keyword}%', keyword))
    patients = cursor.fetchall()
    for patient in patients:
        print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Admission Date: {patient[4]}, Discharge Date: {patient[5]}")

def display_menu():
    print("\nHospital Management System Menu:")
    print("1. Add Patient")
    print("2. Discharge Patient")
    print("3. Add Medical Record")
    print("4. Update Patient Information")
    print("5. Search Patients")
    print("6. View All Patients")
    print("7. Patient Statistics")
    print("8. View Medical Records")
    print("9. Sort Patients by Age")
    print("0. Exit")

def calculate_average_age():
    cursor.execute('SELECT AVG(age) FROM patients WHERE discharge_date IS NOT NULL')
    average_age = cursor.fetchone()[0]
    if average_age is not None:
        print(f"\nAverage age of discharged patients: {average_age:.2f}")
    else:
        print("No discharged patients found.")
        
def view_medical_records(patient_id):
    cursor.execute('''
    SELECT patients.name, medical_records.id, medical_records.diagnosis, medical_records.prescription
    FROM patients
    LEFT JOIN medical_records ON patients.id = medical_records.patient_id
    WHERE patients.id = ?
    ''', (patient_id,))
    
    records = cursor.fetchall()
    if records:
        patient_name = records[0][0]
        print(f"Medical Records for {patient_name}:")
        for record in records:
            print(f"Record ID: {record[1]}, Diagnosis: {record[2]}, Prescription: {record[3]}")
    else:
        print("No medical records found for this patient.")


def sort_patients_by_age():
    cursor.execute('SELECT * FROM patients ORDER BY age DESC')
    patients = cursor.fetchall()
    if patients:
        print("\nPatients Sorted by Age (Descending):")
        for patient in patients:
            discharge_date = patient[5] if patient[5] else "Not discharged"
            print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Admission Date: {patient[4]}, Discharge Date: {discharge_date}")
    else:
        print("No patients found.")

def view_patients():
    cursor.execute('SELECT * FROM patients WHERE discharge_date IS NULL')
    patients = cursor.fetchall()
    if patients:
        print("\nCurrent Patients:")
        for patient in patients:
            print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Admission Date: {patient[4]}")
    else:
        print("No current patients found.")

# Simple command-line interface
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ")

        if choice == '0':
            print("Exiting Hospital Management System. Goodbye!")
            break

        elif choice == '1':
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            gender = input("Enter patient gender: ")
            add_patient(name, age, gender)

        elif choice == '2':
            patient_id = int(input("Enter patient ID to discharge: "))
            discharge_patient(patient_id)

        elif choice == '3':
            patient_id = int(input("Enter patient ID for medical record: "))
            diagnosis = input("Enter diagnosis: ")
            prescription = input("Enter prescription: ")
            add_medical_record(patient_id, diagnosis, prescription)

        elif choice == '4':
            patient_id = int(input("Enter patient ID to update information: "))
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            new_gender = input("Enter new gender: ")
            update_patient_info(patient_id, new_name, new_age, new_gender)

        elif choice == '5':
            keyword = input("Enter patient name or ID to search: ")
            search_patients(keyword)

        elif choice == '6':
            view_patients()

        elif choice == '7':
            calculate_average_age()

        elif choice == '8':
            patient_id = int(input("Enter patient ID to view medical records: "))
            view_medical_records(patient_id)

        elif choice == '9':
            sort_patients_by_age()

        else:
            print("Invalid choice. Please enter a number between 0 and 9.")
if __name__=="__main__":
    main()