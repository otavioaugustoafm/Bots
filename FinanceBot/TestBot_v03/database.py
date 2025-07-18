import sqlite3
from datetime import date

def createDatabase():
    try:
        print("Criando/Verificando a tabela \"Expenses\".")
        connection = sqlite3.connect("Expense.db") # makes the connection with the db
        cursor = connection.cursor() # creates the cursor that executes the SQL commands
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Value REAL NOT NULL,
                Type VARCHAR(11),
                Date DATE NOT NULL,
                Description TEXT NOT NULL
            )
        """)
        connection.commit() # commit the creation of the table
        connection.close() # close the connection with db
        print("Tabela criada/verificada com sucesso.")
        return
    except Exception as e:
        print("Algum erro ocorreu durante a criação/verificação da tabela.")
        return 
        
def store(expenseData):
    try:
        print("Armazenando um gasto.")
        connection = sqlite3.connect("Expense.db") # makes the connection with the db
        cursor = connection.cursor() # creates the cursor that executes the SQL commands
        if expenseData["Date"] is None: # check if the field "Date" exists and uses the current date if it doesn't exists
            cursor.execute("""
                INSERT INTO Expenses (Value, Type, Date, Description)
                VALUES (?, ?, DATE('now'), ?)
            """, expenseData["Value"], expenseData["Value"], expenseData["Description"])
        else:
            cursor.execute("""
                INSERT INTO Expense (Value, Type, Date, Description)
                VALUES (?, ?, ?, ?)
            """, (expenseData["Value"], expenseData["Value"], expenseData["Date"], expenseData["Description"]))
        connection.commit() # commit the insertion on the table
        connection.close() # closes the connection with the db
    except Exception as e:
        return "Algum erro ocorreu durante a inserção do gasto."

def showAll():
    try:
        print("Mostrando todos os gastos.")
        connection = sqlite3.connect("Expense") # makes the connection with the db
        cursor = connection.cursor() # creates the cursos that executes the SQL commands
        cursor.execute("""
            SELECT Value, Type, Date, Description 
            FROM Expenses
            ORDER BY date ASC
        """)
        results = cursor.fetchall() # results receives the result of the SELECT command
        connection.close() # closes the connection with the db
        return results
    except Exception as e:
        return "Algum erro ocorreu ao buscar por todos os gastos."
    
def filter(filters):
    try:
        print("Filtrando.")
        connection = sqlite3.connect("Expenses") # makes the connection with the db
        cursor = connection.cursor() # creates the cursos that executes the SQL commands
        if "Type" in filters: # if the filter is only by type executes this SELECT
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Type == (?) 
            """, (filters["Type"],))
        results = cursor.fetchall() # results receives the result of the SELECT command
        connection.close() # closes the connection with the db
        return results
    except Exception as e:
        return "Algum erro ocorreu ao filtrar."