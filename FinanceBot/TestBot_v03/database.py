import sqlite3

def createTable():
    try:
        connection = sqlite3.connect(r"FinanceBot\TestBot_v03\Expense.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                ID_Expense INTEGER PRIMARY KEY AUTOINCREMENT,
                Value REAL NOT NULL,
                Type VARCHAR(11) NOT NULL,
                Date DATE,
                Description TEXT
            )
        """)
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(e)
        return False

def store(dict):
    try:
        print(dict)
        connection = sqlite3.connect(r"FinanceBot\TestBot_v03\Expense.db")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Expenses (Value, Type, Date, Description)
            VALUES (?,?,?,?)
        """, (dict["Value"], dict["Type"], dict["Date"], dict["Description"]))
        connection.commit()
        connection.close()
        print("Gasto armazenado com sucesso.")
        return True
    except Exception as e:
        print(e)
        return False

def showAll():
    try:
        connection = sqlite3.connect(r"FinanceBot\TestBot_v03\Expense.db")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Value, Type, Date, Description
            FROM Expenses
            ORDER BY Date ASC
        """)
        results = cursor.fetchall()
        connection.close()
        print("Consulta de todos gastos realizada com sucesso.")
        return results
    except Exception as e:
        print(e)
        return False