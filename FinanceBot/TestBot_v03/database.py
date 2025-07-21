import sqlite3
from datetime import date

def createDatabase():
    try:
        print("Criando/Verificando a tabela \"Expense\".")
        connection = sqlite3.connect("Expense.db") # makes the connection with the db
        cursor = connection.cursor() # creates the cursor that executes the SQL commands
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Value REAL NOT NULL,
                Type VARCHAR(11),
                Date DATE NOT NULL,
                Description TEXT
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
                INSERT INTO Expense (Value, Type, Date, Description)
                VALUES (?, ?, DATE('now'), ?)
            """, (expenseData["Value"], expenseData["Type"], expenseData["Description"]))
        else:
            cursor.execute("""
                INSERT INTO Expense (Value, Type, Date, Description)
                VALUES (?, ?, ?, ?)
            """, (expenseData["Value"], expenseData["Type"], expenseData["Date"], expenseData["Description"]))
        connection.commit() # commit the insertion on the table
        connection.close() # closes the connection with the db
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(e)
        return "Algum erro ocorreu durante a inserção do gasto."

def showAll():
    try:
        print("Pesquisando no banco de dados.")
        connection = sqlite3.connect("Expense.db") # makes the connection with the db
        cursor = connection.cursor() # creates the cursos that executes the SQL commands
        cursor.execute("""
            SELECT Value, Type, Date, Description 
            FROM Expense
            ORDER BY date ASC
        """)
        results = cursor.fetchall() # results receives the result of the SELECT command
        connection.close() # closes the connection with the db
        print("Busca completa.")
        return results
    except Exception as e:
        print(e)
        return "Algum erro ocorreu ao buscar por todos os gastos."
    
