import sqlite3
from datetime import date

def createDataBase():
    try:
        # makes the connection with the db and create the .db in case it doesn't exists. 
        # "connection" receives an object and it will be used as a communication channel 
        connection = sqlite3.connect("expenses.db")
        # creates the "cursor", the object that executes the SQL commands
        cursor = connection.cursor()
        # executes the CREATE TABLE if it doesn't exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL NOT NULL, 
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                date DATE NOT NULL
            )
        """)
        # commit the creation of the table and closes it
        connection.commit()
        connection.close()
        print("Tabela criada/verificada com sucesso.")
    except Exception as e:
        print("Erro ao criar ou verificar a tabela.")

def storeData(data):
    try:
        # makes the connection with the db and create the .db in case it doesn't exists. 
        # "connection" receives an object and it will be used as a communication channel 
        connection = sqlite3.connect("expenses.db")
        # creates the "cursor", the object that executes the SQL commands
        cursor = connection.cursor()
        # execute the expense data insertion on the table
        if "date" in data:
            cursor.execute(""" 
                INSERT INTO Expenses (value, type, description, date) 
                VALUES (?, ?, ?, ?)
            """, (data["value"], data["type"], data["description"], data["date"]))
        else:
            cursor.execute(""" 
                INSERT INTO Expenses (value, type, description, date) 
                VALUES (?, ?, ?, DATE('now'))
            """, (data["value"], data["type"], data["description"]))
        # commits the command and closes the connection
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        # in case it fails
        print("A inserção de dados falhou.")
        return False

def showAllData():
    try:
        # makes the connection with the db and create the .db in case it doesn't exists. 
        # "connection" receives an object and it will be used as a communication channel 
        connection = sqlite3.connect("expenses.db")
        # creates the "cursor", the object that executes the SQL commands
        cursor = connection.cursor()
        # execute the search on the table for all tuples
        cursor.execute(""" 
            SELECT value, type, description, date
            FROM Expenses
            ORDER BY date DESC
        """)
        # results receives all the tuples on the table expenses
        results = cursor.fetchall()
        # close the connection. 
        # no need to commit because it was a search
        connection.close()
        return results
    except Exception as e:
        return False
    
def filterByType(typeRead):
    try:
        # makes the connection with the db and create the .db in case it doesn't exists. 
        # "connection" receives an object and it will be used as a communication channel 
        connection = sqlite3.connect("expenses.db")
        # creates the "cursor", the object that executes the SQL commands
        cursor = connection.cursor()
        # execute the search on the table for all tuples
        cursor.execute(""" 
            SELECT value, type, description, date
            FROM Expenses
            WHERE type = (?)
            ORDER BY date DESC
        """, (typeRead,))
        # results receives all the tuples on the table expenses
        results = cursor.fetchall()
        # close the connection. 
        # no need to commit because it was a search
        connection.close()
        return results
    except Exception as e:
        return False

def filterByDate(formatedDate):
    try:
        connection = sqlite3.connect("expenses.db")
        # creates the "cursor", the object that executes the SQL commands
        cursor = connection.cursor()
        # execute the search on the table for all tuples
        dates = formatedDate.split(" ")
        if len(dates) == 1:
            date1 = dates[0]
            cursor.execute(""" 
            SELECT value, type, description, date
            FROM Expenses
            WHERE date == (?)
            ORDER BY date DESC
        """, (date1,))
        elif len(dates) == 2:
            date1 = dates[0]
            date2 = dates[1]
            cursor.execute(""" 
            SELECT value, type, description, date
            FROM Expenses
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date DESC
        """, (date1, date2))
        # results receives all the tuples on the table expenses
        results = cursor.fetchall()
        # close the connection. 
        # no need to commit because it was a search
        connection.close()
        return results
    except Exception as e:
        return False
