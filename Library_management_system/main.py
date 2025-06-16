import sqlite3
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, copies=1):
        self.title = title
        self.author = author
        self.copies = copies
        self.available_copies = copies
        self.reserved_users = set()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.borrowed_books = {}
        self.reserved_books = set()

class Library:
    def __init__(self):
        self.connection = sqlite3.connect("library_database.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                title TEXT PRIMARY KEY,
                                author TEXT,
                                copies INTEGER,
                                available_copies INTEGER,
                                reserved_users TEXT
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT,
                                borrowed_books TEXT,
                                reserved_books TEXT
                            )''')
        self.connection.commit()

        self.catalog = {}
        self.users = {}

        # Load existing data from the database
        self.load_books_from_db()
        self.load_users_from_db()

    def load_books_from_db(self):
        self.cursor.execute("SELECT * FROM books")
        books_data = self.cursor.fetchall()
        for book_data in books_data:
            title, author, copies, available_copies, reserved_users = book_data
            book = Book(title, author, copies)
            book.available_copies = available_copies
            book.reserved_users = set(reserved_users.split(','))
            self.catalog[title] = book

    def load_users_from_db(self):
        self.cursor.execute("SELECT * FROM users")
        users_data = self.cursor.fetchall()
        for user_data in users_data:
            username, password, borrowed_books, reserved_books = user_data
            user = User(username, password)
            user.borrowed_books = dict(item.split(':') for item in borrowed_books.split(',') if ':' in item)
            user.reserved_books = set(reserved_books.split(','))
            self.users[username] = user

    def __del__(self):
        self.connection.close()

    def add_book(self, title, author, copies=1):
        if title not in self.catalog:
            self.catalog[title] = Book(title, author, copies)
            self.cursor.execute('''INSERT INTO books 
                                (title, author, copies, available_copies, reserved_users)
                                VALUES (?, ?, ?, ?, ?)''',
                                (title, author, copies, copies, ''))
            self.connection.commit()
            print(f"Book '{title}' by {author} added to the catalog.")
        else:
            self.catalog[title].copies += copies
            self.catalog[title].available_copies += copies
            self.cursor.execute('''UPDATE books SET copies=?, available_copies=?
                                WHERE title=?''', (self.catalog[title].copies,
                                                  self.catalog[title].available_copies, title))
            self.connection.commit()
            print(f"Additional {copies} copies of '{title}' added to the catalog.")

    def remove_book(self, title):
        if title in self.catalog:
            del self.catalog[title]
            self.cursor.execute("DELETE FROM books WHERE title=?", (title,))
            self.connection.commit()
            print(f"Book '{title}' removed from the catalog.")
        else:
            print(f"Book '{title}' is not in the catalog.")

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            self.cursor.execute('''INSERT INTO users (username, password, borrowed_books, reserved_books)
                                VALUES (?, ?, ?, ?)''', (username, password, '', ''))
            self.connection.commit()
            print(f"User '{username}' registered successfully.")
        else:
            print(f"Username '{username}' is already taken.")

    def search_books(self, keyword):
        matching_books = [book.title for book in self.catalog.values() if keyword.lower() in book.title.lower()]
        if matching_books:
            print(f"Matching books for '{keyword}': {', '.join(matching_books)}")
        else:
            print(f"No books found for '{keyword}'.")

    def display_user_details(self, username):
        user = self.users.get(username)
        if user:
            print(f"User Details for '{username}':")
            if user.borrowed_books:
                print("Borrowed Books:")
                for book, due_date in user.borrowed_books.items():
                    print(f"- {book} (Due Date: {due_date})")
            else:
                print("No books currently borrowed.")
            if user.reserved_books:
                print("Reserved Books:", ', '.join(user.reserved_books))
            else:
                print("No books currently reserved.")
        else:
            print("Invalid username.")

    def borrow_book(self, username, title):
        user = self.users.get(username)
        if user and title in self.catalog:
            book = self.catalog[title]
            if book.available_copies > 0:
                book.available_copies -= 1
                due_date = datetime.now() + timedelta(days=14)  # Assuming a 2-week borrowing period
                user.borrowed_books[title] = due_date.strftime("%Y-%m-%d")
                self.cursor.execute('''UPDATE books SET available_copies=?
                                    WHERE title=?''', (book.available_copies, title))
                self.connection.commit()
                self.cursor.execute('''UPDATE users SET borrowed_books=?
                                    WHERE username=?''', (':'.join([f"{b}:{d}" for b, d in user.borrowed_books.items()]), username))
                self.connection.commit()
                print(f"Book '{title}' borrowed successfully by {username}.")
                print(f"Due Date: {due_date.strftime('%Y-%m-%d')}")
            else:
                print(f"Sorry, all copies of '{title}' are currently checked out.")
                print("Would you like to be notified when it's available?")
                choice = input("Enter 'yes' or 'no': ").lower()
                if choice == 'yes':
                    user.reserved_books.add(title)
                    self.catalog[title].reserved_users.add(username)
                    self.cursor.execute('''UPDATE books SET reserved_users=?
                                        WHERE title=?''', (','.join(self.catalog[title].reserved_users), title))
                    self.connection.commit()
                    self.cursor.execute('''UPDATE users SET reserved_books=?
                                        WHERE username=?''', (','.join(user.reserved_books), username))
                    self.connection.commit()
                    print(f"Book '{title}' reserved for {username}.")
                    print(f"You will be notified when it's available.")
                else:
                    print("Book not reserved.")
        else:
            print("Invalid username or book title.")

    def return_book(self, username, title):
        user = self.users.get(username)
        if user and title in user.borrowed_books:
            book = self.catalog[title]
            book.available_copies += 1
            del user.borrowed_books[title]
            self.cursor.execute('''UPDATE books SET available_copies=?
                                WHERE title=?''', (book.available_copies, title))
            self.connection.commit()
            self.cursor.execute('''UPDATE users SET borrowed_books=?
                                WHERE username=?''', (':'.join([f"{b}:{d}" for b, d in user.borrowed_books.items()]), username))
            self.connection.commit()
            print(f"Book '{title}' returned successfully by {username}.")
            # Check if there are reserved users for this book
            if book.reserved_users:
                reserved_user = book.reserved_users.pop()
                user_to_notify = self.users.get(reserved_user)
                if title in user_to_notify.reserved_books:
                    user_to_notify.reserved_books.remove(title)
                    self.cursor.execute('''UPDATE users SET reserved_books=?
                                        WHERE username=?''', (','.join(user_to_notify.reserved_books), reserved_user))
                    self.connection.commit()
                    print(f"{reserved_user} can now borrow the reserved book '{title}'.")
        else:
            print("Invalid username or book title.")

    def calculate_fine(self, due_date):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        today = datetime.now()
        overdue_days = max(0, (today - due_date).days)
        fine_rate = 0.50  # Fine rate per day
        fine_amount = round(overdue_days * fine_rate, 2)
        return fine_amount

    def view_popular_books(self, top_n=5):
        sorted_books = sorted(self.catalog.values(), key=lambda x: x.copies - x.available_copies, reverse=True)
        print(f"Most Popular Books:")
        for i, book in enumerate(sorted_books[:top_n]):
            print(f"{i+1}. {book.title} by {book.author} - Available Copies: {book.available_copies}")

# Example Usage:
library = Library()

while True:
    print("\n==== Library Management System ====")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Register User")
    print("4. Search Books")
    print("5. Display User Details")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. Calculate Fine")
    print("9. View Popular Books")
    print("0. Exit")
    choice = input("Enter your choice (0-9): ")

    if choice == '1':
        title = input("Enter book title: ")
        author = input("Enter author: ")
        copies = int(input("Enter number of copies: "))
        library.add_book(title, author, copies)

    elif choice == '2':
        title = input("Enter book title to remove: ")
        library.remove_book(title)

    elif choice == '3':
        username = input("Enter username: ")
        password = input("Enter password: ")
        library.register_user(username, password)

    elif choice == '4':
        keyword = input("Enter keyword to search for books: ")
        library.search_books(keyword)

    elif choice == '5':
        username = input("Enter username to display details: ")
        library.display_user_details(username)

    elif choice == '6':
        username = input("Enter your username: ")
        title = input("Enter the title of the book you want to borrow: ")
        library.borrow_book(username, title)

    elif choice == '7':
        username = input("Enter your username: ")
        title = input("Enter the title of the book you want to return: ")
        library.return_book(username, title)

    elif choice == '8':
        username = input("Enter your username: ")
        title = input("Enter the title of the borrowed book: ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")
        fine = library.calculate_fine(due_date)
        print(f"Fine for overdue book: ${fine}")

    elif choice == '9':
        library.view_popular_books()

    elif choice == '0':
        print("Exiting Library Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 0 and 9.")