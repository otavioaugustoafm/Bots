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
    
def showFiltered(filters):
    try:
        connection = sqlite3.connect(r"FinanceBot\TestBot_v03\Expense.db")
        cursor = connection.cursor()
        if filters["Type"] is not None and filters["Date1"] is not None and filters["Date2"] is not None:
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Type == ?
                AND Date BETWEEN ? AND ?
                ORDER BY Date ASC
            """, (filters["Type"], filters["Date1"], filters["Date2"]))
        elif filters["Date1"] is not None and filters["Date2"] is not None:
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Date BETWEEN ? AND ?
                ORDER BY Date ASC
            """, (filters["Date1"], filters["Date2"]))
        elif filters["Date1"] is not None and filters["Type"] is not None:
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Date == ?
                AND Type == ?
                ORDER BY Date ASC
            """, (filters["Date1"], filters["Type"]))
        elif filters["Date1"] is not None:
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Date == ?
                ORDER BY Date ASC
            """, (filters["Date1"],))
        elif filters["Type"] is not None:
            cursor.execute("""
                SELECT Value, Type, Date, Description
                FROM Expenses
                WHERE Type == ?
                ORDER BY Date ASC
            """, (filters["Type"],))
        results = cursor.fetchall()
        connection.close()
        print("Consulta de gastos filtrados realizada com sucesso.")
        return results
    except Exception as e:
        print(e)
        return False

def showSum(filters):
    try:
        connection = sqlite3.connect(r"FinanceBot\TestBot_v03\Expense.db")
        cursor = connection.cursor()
        if filters["Type"] is not None and filters["Date1"] is not None and filters["Date2"] is not None:
            cursor.execute("""
                SELECT SUM(Value)
                FROM Expenses
                WHERE Type == ?
                AND Date BETWEEN ? AND ?
            """, (filters["Type"], filters["Date1"], filters["Date2"]))
        elif filters["Date1"] is not None and filters["Date2"] is not None:
            cursor.execute("""
                SELECT SUM(Value)
                FROM Expenses
                WHERE Date BETWEEN ? AND ?
            """, (filters["Date1"], filters["Date2"]))
        elif filters["Date1"] is not None and filters["Type"] is not None:
            cursor.execute("""
                SELECT SUM(Value)
                FROM Expenses
                WHERE Date == ?
                AND Type == ?
            """, (filters["Date1"], filters["Type"]))
        elif filters["Date1"] is not None:
            cursor.execute("""
                SELECT SUM(Value)
                FROM Expenses
                WHERE Date == ?
            """, (filters["Date1"],))
        elif filters["Type"] is not None:
            cursor.execute("""
                SELECT SUM(Value)
                FROM Expenses
                WHERE Type == ?
            """, (filters["Type"],))
        results = cursor.fetchone()
        connection.close()
        print("Consulta de soma de gastos filtrados realizada com sucesso.")
        return results
    except Exception as e:
        print(e)
        return False