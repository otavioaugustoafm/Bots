import sqlite3

def createTable():
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Value INTEGER NOT NULL,
                Type VARCHAR(11) NOT NULL,
                Date DATE NOT NULL,
                Description VARCHAR(255)
                )
        """)
        connection.commit()
        connection.close()
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(f"Erro ao criar/verificar tabela:\n{e}")
        return False
    
def store(dict):
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        Value = dict["Value"]; Type = dict["Type"]; Date = dict["Date"]; Description = dict["Description"]
        cursor.execute("""
            INSERT INTO Expenses (Value, Type, Date, Description)
            VALUES (?, ?, ?, ?)
        """, (Value, Type, Date, Description))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Erro ao armazenar gasto:\n{e}")
        return False
    
def showAll(command):
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        sqlCommand = "SELECT "
        if command == "/1":
            sqlCommand += "Value, Type, Date, Description "
        elif command == "/4":
            sqlCommand += "* "
        sqlCommand += "FROM Expenses ORDER BY Date ASC"
        cursor.execute(sqlCommand)
        results = cursor.fetchall()
        connection.close()
        return results
    except Exception as e:
        print(f"Erro ao mostrar todos os gastos:\n{e}")
        return False