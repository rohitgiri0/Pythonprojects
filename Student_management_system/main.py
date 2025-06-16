import sqlite3

class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

class StudentInformationSystem:
    def __init__(self, db_file='students.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                grade TEXT
            )
        ''')
        self.conn.commit()

    def add_student(self, student_id, name, age, grade):
        student = Student(student_id, name, age, grade)
        self.cursor.execute('''
            INSERT INTO students (student_id, name, age, grade)
            VALUES (?, ?, ?, ?)
        ''', (student.student_id, student.name, student.age, student.grade))
        self.conn.commit()
        print(f"Student {student.name} added successfully.")

    def display_students(self):
        self.cursor.execute('SELECT * FROM students')
        students = self.cursor.fetchall()

        if not students:
            print("No students in the system.")
            return

        print("Student Information:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")

    def search_student(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student = self.cursor.fetchone()

        if student:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
        else:
            print(f"No student found with ID {student_id}.")

    def update_student(self, student_id, new_name, new_age, new_grade):
        self.cursor.execute('''
            UPDATE students
            SET name = ?, age = ?, grade = ?
            WHERE student_id = ?
        ''', (new_name, new_age, new_grade, student_id))
        self.conn.commit()
        print(f"Student with ID {student_id} updated successfully.")

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()
        print(f"Student with ID {student_id} deleted successfully.")

    def sort_students(self, key='name'):
        valid_keys = ['name', 'age', 'grade']
        if key not in valid_keys:
            print(f"Invalid sorting key. Available keys: {', '.join(valid_keys)}")
            return

        self.cursor.execute(f'SELECT * FROM students ORDER BY {key}')
        students = self.cursor.fetchall()

        if not students:
            print("No students in the system.")
            return

        print(f"Students sorted by {key}:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")

    def average_age(self):
        self.cursor.execute('SELECT AVG(age) FROM students')
        avg_age = self.cursor.fetchone()[0]
        print(f"Average age of students: {avg_age:.2f}")

    def display_statistics(self):
        self.cursor.execute('SELECT COUNT(*), MIN(age), MAX(age), AVG(age) FROM students')
        statistics = self.cursor.fetchone()
        print(f"Number of students: {statistics[0]}")
        print(f"Youngest student age: {statistics[1]}")
        print(f"Oldest student age: {statistics[2]}")
        print(f"Average age of students: {statistics[3]:.2f}")

    def close_connection(self):
        self.conn.close()

# Interactive menu
def main():
    sis = StudentInformationSystem()

    while True:
        print("\nStudent Information System Menu:")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort Students")
        print("7. Average Age")
        print("8. Display Statistics")
        print("0. Exit")

        choice = input("Enter your choice (0-8): ")

        if choice == '0':
            sis.close_connection()
            break
        elif choice == '1':
            sis.add_student(
                int(input("Enter student ID: ")),
                input("Enter student name: "),
                int(input("Enter student age: ")),
                input("Enter student grade: ")
            )
        elif choice == '2':
            sis.display_students()
        elif choice == '3':
            student_id = int(input("Enter student ID to search: "))
            sis.search_student(student_id)
        elif choice == '4':
            student_id = int(input("Enter student ID to update: "))
            sis.update_student(
                student_id,
                input("Enter new student name: "),
                int(input("Enter new student age: ")),
                input("Enter new student grade: ")
            )
        elif choice == '5':
            student_id = int(input("Enter student ID to delete: "))
            sis.delete_student(student_id)
        elif choice == '6':
            key = input("Enter sorting key (name/age/grade): ")
            sis.sort_students(key)
        elif choice == '7':
            sis.average_age()
        elif choice == '8':
            sis.display_statistics()
        else:
            print("Invalid choice. Please enter a number between 0 and 8.")

if __name__ == "__main__":
    main()