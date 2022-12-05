import sqlite3 as sql


class Database:
    """
    Class which connects code to database.
    Path to the database inputs by user.
    ...
    Methods:
    -------
    __init__ : connects to the database and creating a cursor to do the actions
    relatively to database.
    path to the database :parameter str path
    ...
    create_table : creates table "contact_book" with columns.
    str contact_name - for contact's name;
    int contact_number - for contact's phone number;
    str contact_email - for contact's email address;
    ...
    add : adds contact's info to the table "contact_book".
    contact's name :parameter name
    contact's number :parameter number
    contact's email :parameter email
    if contact successfully added to the "contact_book" :return "Contact successfully added"
    if contact already exists in the "contact_book" :return "This contact already exists"
    ...
    update : updates info for existing contact.
    Founds contact in table "contact_book" by contact's number.
    Sets contact's new info from user's input.
    for contact's number :parameter number
    if contact's info successfully updated :return "Contact successfully updated"
    if contact doesn't exist in the "contact_book" :return "This contact doesn't exist"
    if new number for the contact is not integer :return "Number is necessary parameter. Enter it correctly"
    ...
    search : search contact in "contact_book" by contact's number.
    for contact's number :parameter number
    if contact doesn't exist in the "contact_book" :return "This contact doesn't exist"
    :return contact: if contacts exists in "contact_book.
    ...
    show : shows all the contact's from "contact_book" or result of the operation.
    ...
    delete : deletes a contact from "contact_book" if contact exists.
    Founds contact by number.
    for contact's number :parameter number
    if contacts was successfully deleted form "contact_book" :return "Contact successfully deleted"
    if contact does not exist in "contact_book" :return "This contact doesn't exist"
    """
    def __init__(self, path):
        self.connect = sql.connect(path)
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_book(
        contact_name TEXT,
        contact_number INT,
        contact_email TEXT);""")
        self.connect.commit()

    def add(self, name, number, email):
        self.cursor.execute(f"""SELECT contact_number FROM contact_book
        WHERE contact_number = {number}""")
        contact = self.cursor.fetchall()
        if len(contact) < 1:
            self.cursor.execute(f"""INSERT INTO contact_book(contact_name, contact_number, contact_email)
            VALUES ('{name}', {number}, '{email}')""")
            self.connect.commit()
            result = "Contact successfully added"
            return print(result)
        else:
            result = "This contact already exists"
            return print(result)

    def update(self, number):
        self.cursor.execute(f"""SELECT * FROM contact_book
        WHERE contact_number = {number}""")
        contact = self.cursor.fetchall()
        if len(contact) > 0:
            print(f"{contact}\nEnter new contact's info")
            new_name = input("New name: ").strip()
            new_number = input("New number: ")
            new_email = input("New email: ").strip()
            try:
                new_number = int(new_number)
                self.cursor.execute(f"""UPDATE contact_book
                SET contact_name = '{new_name}',
                    contact_number = {new_number},
                    contact_email = '{new_email}'
                WHERE contact_number = {number}""")
                self.connect.commit()
                result = "Contact successfully updated"
                return print(result)
            except ValueError:
                print("Number is necessary parameter. Enter it correctly")
                return self.update(number)
        else:
            result = "This contact doesn't exist"
            return print(result)

    def search(self, number):
        self.cursor.execute(f"""SELECT contact_number FROM contact_book
        WHERE contact_number = {number}""")
        contact = self.cursor.fetchall()
        if len(contact) < 1:
            result = "This contact doesn't exist"
            return print(result)
        else:
            return print(contact)

    def show(self):
        self.cursor.execute(f"""SELECT * FROM contact_book""")
        contacts = self.cursor.fetchall()
        if len(contacts) < 1:
            result = "No contacts yet"
            print(result)
        else:
            for key, contact in enumerate(contacts, start=1):
                print(key, contact)

    def delete(self, number):
        self.cursor.execute(f"""SELECT contact_number FROM contact_book
        WHERE contact_number = {number}""")
        contact = self.cursor.fetchall()
        if len(contact) > 0:
            self.cursor.execute(f"""DELETE FROM contact_book
            WHERE contact_number = {number}""")
            self.connect.commit()
            result = "Contact successfully deleted"
            return print(result)
        else:
            result = "This contact doesn't exist"
            return print(result)


def commands(database):
    """
    Shows commands to user, ang gets a number of the command from the user.
    Gets a database and returns it to the next function main().
    Commands:
    1 for adding a contact to "contact_book"
    2 for updating contact's info in "contact_info"
    3 for searching a contact in "contact_info"
    4 for showing all the contacts from "contact_book"
    5 for deleting contact from "contact_book"
    ...
    database object :parameter database
    starts main(), if number of the command entered by user is integer :return main(command, database)
    restarts itself, if number of the command by user entered incorrectly :return commands(database)
    """
    print("""Choose the command for your Contact Book:
    1. Add a contact
    2. Update contact's info
    3. Search a contact
    4. Show all contacts
    5. Delete a contact""")
    try:
        command = int(input("Enter number of the command: "))
        return main(command, database)
    except ValueError:
        print("Number of the command entered incorrectly. Try again")
        return commands(database)


def main(command, database):
    """
    Gets number of the command and acts according to it.
    ...
    number of the command :parameter command
    database object :parameter database
    restarts function commands(), so user can choose next action :return commands(database)
    """
    if command == 1:
        name = input("Contact's name: ").strip()
        number = check_integer(input("Contact's number: "), main, 1, database)
        email = input("Contact's email: ").strip()
        database.add(name, number, email)
        return commands(database)
    elif command == 2:
        number = check_integer(input("Enter contact's number, whose info you want to update: "), main, 2, database)
        database.update(number)
        return commands(database)
    elif command == 3:
        number = check_integer(input("Contact's number: "), main, 3, database)
        database.search(number)
        return commands(database)
    elif command == 4:
        database.show()
        return commands(database)
    elif command == 5:
        number = check_integer(input("Contact's number: "), main, 5, database)
        database.delete(number)
        return commands(database)
    else:
        print("Wrong command entered. Try again.")
        return commands(database)


def check_integer(num, function, arg, database):
    """
    Checks if number is integer.
    ...
    number to check :parameter num
    function to start again :parameter  function
    argument for the function :parameter  arg
    database object for the function :parameter  database
    if number is integer :return int(num)
    starts definitive function if number is not integer :returns function(arg, database)
    """
    try:
        num = int(num)
        return num
    except ValueError:
        print("Number is necessary parameter. Enter it correctly")
        return function(arg, database)


if __name__ == "__main__":
    database_path = input("Enter path to open or create database: ")
    contacts_db = Database(database_path)
    contacts_db.create_table()
    commands(contacts_db)