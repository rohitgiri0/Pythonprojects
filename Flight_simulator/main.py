import sqlite3
from getpass import getpass

conn=sqlite3.connect("flights_info.db")
cursor=conn.cursor()

#CREATING TABLES

cursor.execute('''
               CREATE TABLE IF NOT EXISTS flights(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   flight_number TEXT,
                   origin TEXT,
                   destination TEXT,
                   capacity INTEGER
               )
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS passengers(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   flight_id INTEGER,
                   passenger_name TEXT,
                   FOREIGN KEY(flight_id) REFERENCES flights(id)
               )
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT
               )
               ''')

# TESTING 

cursor.execute("INSERT INTO users(username,password) VALUES (?,?)",("admin","admin123"))

conn.commit()

class flightSimulator:
    def __init__(self):
        self.current_user=None
        
    def add_user(self):
        name=input("enter username: ")
        password=input("create a password: ")
        cursor.execute('''INSERT INTO users (username,password) VALUES (?,?)''',(name,password))

    def delete_user(self,name,password):
        cursor.execute("DELETE FROM users WHERE username=? AND password=?",(name,password))
        conn.commit()
        if cursor.rowcount > 0:
            print("User deleted successfully!")
        else:
            print("No matching user found.")

    def authenticate_user(self):
        max_attempts=3
        for _ in range(max_attempts):
            username=input("enter your username: ")
            password=getpass("enter your password: ")

            cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

            user=cursor.fetchone()

            if user:
                print("Authentication successful!")
                self.current_user=username
                return
            print("Authentication failed. please try again")
            
        print(f"Exceeded maximum authentication attempts. Exiting...")
        exit()
        
    def create_flight(self,flight_number,origin,destination,capacity):
        cursor.execute('''
                       INSERT INTO flights (flight_number,origin,destination,capacity) VALUES (?,?,?,?)
                       ''',(flight_number,origin,destination,capacity))
        conn.commit()
                    
        print("flight created successfully")
        
    def display_flights(self):
        cursor.execute("SELECT * FROM flights")
        flights=cursor.fetchall()
        
        if not flights:
            print("there are no flights!")
        else:
            for index,flight in enumerate(flights,start=1):
                print(f"{index}. Flight id : {flight[0]}, Flight Number : {flight[1]}, Origin : {flight[2]}, Destination : {flight[3]}, Capacity : {flight[4]}")
                
    def book_seat(self,flight_id,p_name):
        cursor.execute("SELECT capacity FROM flights WHERE id=?",(flight_id))
        capacity=cursor.fetchone()

        if capacity and capacity[0]>0:
            cursor.execute('''
                           INSERT INTO passengers(flight_id,passenger_name) VALUES (?,?)''',(flight_id,p_name))
                        
            cursor.execute('''
                           UPDATE flights SET capacity=capacity-1 WHERE id=?
                           ''',(flight_id))
            conn.commit()
            print(f"seat booked for {p_name} on flight {flight_id}")
            
    def display_passenger(self,flight_id):
        cursor.execute("SELECT passenger_name FROM passengers WHERE flight id=?",(flight_id))
        passengers=cursor.fetchall()
        if not passengers:
            print("NO passengers booked for this flight.")
        else: 
            print(f"passenger booked for flight id: {flight_id}")
            for index,passenger in enumerate(passengers):
                print(f"{index}. passenger[0]")
    
    def run_system(self):
        self.authenticate_user()
        
        while True:
            print("\nFlight Reservation System Menu:")
            print("1. Create Flight")
            print("2. Display Flights")
            print("3. Book Seat")
            print("4. Display Passengers for a Flight")
            print("5. Exit")
            print("6. Create a user")
            print("7. Delete a user")

            choice = input("Enter your choice: ")

            if choice == "1":
                flight_number = input("Enter flight number: ")
                origin = input("Enter origin: ")
                destination = input("Enter destination: ")
                capacity = int(input("Enter capacity: "))
                self.create_flight(flight_number, origin, destination, capacity)

            elif choice == "2":
                self.display_flights()

            elif choice == "3":
                self.display_flights()
                flight_id = int(input("Enter the Flight ID to book a seat: "))
                passenger_name = input("Enter passenger name: ")
                self.book_seat(flight_id, passenger_name)

            elif choice == "4":
                self.display_flights()
                flight_id = int(input("Enter the Flight ID to display passengers: "))
                self.display_passengers(flight_id)

            elif choice == "5":
                print("Exiting Flight Reservation System. Goodbye!")
                break
            
            elif choice=="6":
                self.add_user()
                
            elif choice=="7":
                name=input("enter username to delete: ")
                password=input("Password required to delete user: ")
                self.delete_user(name,password)
            
            else:
                print("Invalid choice. Please try again.") 
                
if __name__=="__main__":
    flight_system=flightSimulator()
    flight_system.run_system()
    
    