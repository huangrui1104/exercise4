import sqlite3

# Create a connection to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create tables: Books, Users, and Reservations
c.execute('''CREATE TABLE IF NOT EXISTS Books
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
             (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT,
             FOREIGN KEY (BookID) REFERENCES Books(BookID),
             FOREIGN KEY (UserID) REFERENCES Users(UserID))''')

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")
    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

# Function to find a book's details based on BookID
def find_book_details():
    book_id = input("Enter BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()
    if book:
        print("Book Details:")
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
        reservation = c.fetchone()
        if reservation:
            print("Reserved by:")
            user_id = reservation[2]
            c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
            user = c.fetchone()
            print("UserID:", user[0])
            print("Name:", user[1])
            print("Email:", user[2])
        else:
            print("Not reserved by anyone.")
    else:
        print("Book not found in the database.")

# Function to find a book's reservation status based on different criteria
def find_reservation_status():
    text = input("Enter BookID, Title, UserID, or ReservationID: ")
    if text.startswith("LB"):
        c.execute("SELECT * FROM Books WHERE BookID=?", (text,))
        book = c.fetchone()
        if book:
            book_id = book[0]
            c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
            reservation = c.fetchone()
            if reservation:
                print("Book is reserved.")
            else:
                print("Book is not reserved.")
        else:
            print("Book not found in the database.")
    elif text.startswith("LU"):
        c.execute("SELECT * FROM Users WHERE UserID=?", (text,))
        user = c.fetchone()
        if user:
            user_id = user[0]
            c.execute("SELECT * FROM Reservations WHERE UserID=?", (user_id,))
            reservation = c.fetchone()
            if reservation:
                print("User has a reserved book.")
            else:
                print("User has no reserved books.")
        else:
            print("User not found in the database.")
    elif text.startswith("LR"):
        c.execute("SELECT * FROM Reservations WHERE ReservationID=?", (text,))
        reservation = c.fetchone()
        if reservation:
            print("Reservation exists.")
        else:
            print("Reservation not found in the database.")
    else:
        c.execute("SELECT * FROM Books WHERE Title=?", (text,))
        books = c.fetchall()
        if books:
            print("Books found with the given title:")
            for book in books:
                print("BookID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("ISBN:", book[3])
                print("Status:", book[4])
        else:
            print("No books found with the given title.")

# Function to find all the books in the database
def find_all_books():
    c.execute("SELECT * FROM Books")
    books = c.fetchall()
    if books:
        print("All Books in the Database:")
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
    else:
        print("No books found in the database.")

# Function to modify/update book details based on BookID
def modify_book_details():
    book_id = input("Enter BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()
    if book:
        print("Current Book Details:")
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        choice = input("Enter 1 to update reservation status, or any other key to update other details: ")
        if choice == "1":
            status = input("Enter new reservation status: ")
            c.execute("UPDATE Books SET Status=? WHERE BookID=?", (status, book_id))
            c.execute("UPDATE Reservations SET ReservationStatus=? WHERE BookID=?", (status, book_id))
            conn.commit()
            print("Reservation status updated successfully!")
        else:
            title = input("Enter new Title: ")
            author = input("Enter new Author: ")
            isbn = input("Enter new ISBN: ")
            c.execute("UPDATE Books SET Title=?, Author=?, ISBN=? WHERE BookID=?", (title, author, isbn, book_id))
            conn.commit()
            print("Book details updated successfully!")
    else:
        print("Book not found in the database.")

# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()
    if book:
        c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
        c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found in the database.")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book to the database.")
    print("2. Find a book's detail based on BookID.")
    print("3. Find a book's reservation status.")
    print("4. Find all the books in the database.")
    print("5. Modify/update book details based on BookID.")
    print("6. Delete a book based on BookID.")
    print("7. Exit.")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        modify_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()