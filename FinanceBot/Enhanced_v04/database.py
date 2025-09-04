import sqlite3

def createTable():
    print("--------------------\nCriando ou verificando tabela...")
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
        print("\nTabela OK.\n--------------------")
    except Exception as e:
        print(f"Erro ao criar/verificar tabela:\n{e}")
        return False
    
def store(dict):
    print("Armazenando gasto...")
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
        print("\nGasto armazenado com sucesso.\n--------------------")
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(f"Erro ao armazenar gasto:\n{e}")
        return False
    
def showMonth(date, nextDate):
    print(date)
    print(nextDate)
    print("Mostrando gastos de um mês específico...")
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        sqlCommand = "SELECT * FROM Expenses WHERE (Type = 'Namoro' OR Type = 'Outros' OR Type = 'Compras' OR Type = 'Transporte' OR Type = 'Comida') AND Date BETWEEN ? AND ? ORDER BY Date ASC"
        cursor.execute(sqlCommand, [date, nextDate])
        results1 = cursor.fetchall()
        sqlCommand = "SELECT SUM(Value) FROM Expenses WHERE (Type = 'Namoro' OR Type = 'Outros' OR Type = 'Compras' OR Type = 'Transporte' OR Type = 'Comida') AND Date BETWEEN ? AND ? ORDER BY Date ASC"
        cursor.execute(sqlCommand, [date, nextDate])
        sum1 = cursor.fetchone()
        sqlCommand = "SELECT * FROM Expenses WHERE Type = 'Extra' AND Date BETWEEN ? AND ? ORDER BY Date ASC"
        cursor.execute(sqlCommand, [date, nextDate])
        results2 = cursor.fetchall()
        sqlCommand = "SELECT SUM(Value) FROM Expenses WHERE Type = 'Extra' AND Date BETWEEN ? AND ? ORDER BY Date ASC"
        cursor.execute(sqlCommand, [date, nextDate])
        sum2 = cursor.fetchone()
        print("\nDados exibidos.\n--------------------")
        connection.close()
        return results1, sum1, results2, sum2
    except Exception as e:
        print(f"Erro ao mostrar os gastos de um mês específico:\n{e}")
        return False

def showAll(command):
    print("Mostrando todos gastos...")
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        sqlCommand = "SELECT "
        if command == "/5":
            sqlCommand += "Value, Type, Date, Description "
        elif command == "/4":
            sqlCommand += "* "
        sqlCommand += "FROM Expenses ORDER BY Date ASC"
        cursor.execute(sqlCommand)
        results = cursor.fetchall()
        connection.close()
        print("\nDados exibidos.\n--------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar todos os gastos:\n{e}")
        return False
    
def showFiltered(typeList, dateList):
    print("Mostrando gastos filtrados...")
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        sqlCommand = "SELECT Value, Type, Date, Description FROM Expenses WHERE "
        if typeList:
            for index, filter in enumerate(typeList):
                if index == len(typeList) - 1:
                    sqlCommand += f"Type = '{filter}' "
                    if dateList:
                        sqlCommand += f"AND "
                else:
                    sqlCommand += f"Type = '{filter}' OR "
        if dateList:
            if len(dateList) == 1:
                sqlCommand += f"Date = '{dateList[0]}'"
            elif len(dateList) == 2:
                sqlCommand += f"Date BETWEEN '{dateList[0]}' AND '{dateList[1]}'"
        cursor.execute(sqlCommand)
        results = cursor.fetchall()
        connection.close()
        print("\nDados exibidos.\n--------------------")
        print(sqlCommand)
        return results
    except Exception as e:
        print(f"Erro ao mostrar gastos filtrados:\n{e}")
        return False

def showSum(typeList, dateList):
    print("Mostrando gastos somados...")
    try:
        connection = sqlite3.connect((r"FinanceBot\Enhanced_v04\ExpensesTable.db"))
        cursor = connection.cursor()
        sqlCommand = "SELECT SUM(Value) FROM Expenses WHERE "
        if typeList != []:
            for index, filter in enumerate(typeList):
                if index == len(typeList) - 1:
                    sqlCommand += f"Type = '{filter}' "
                    if dateList:
                        sqlCommand += f"AND "
                else:
                    sqlCommand += f"Type = '{filter}' OR "
        if dateList != []:
            if len(dateList) == 1:
                sqlCommand += f"Date = '{dateList[0]}'"
            elif len(dateList) == 2:
                sqlCommand += f"Date BETWEEN '{dateList[0]}' AND '{dateList[1]}'"
        cursor.execute(sqlCommand)
        results = cursor.fetchone()
        connection.close()
        print("\nDados exibidos.\n--------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar a soma filtrada:\n{e}")
        return False
    
def remove(id):
    print("Removendo gasto...\n")
    try:
        connection = sqlite3.connect(r"FinanceBot\Enhanced_v04\ExpensesTable.db")
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM Expenses 
            WHERE ID = ?
        """,(id,))
        deleted = cursor.rowcount
        if deleted > 0:
            connection.commit()
            connection.close()
            print("Remoção concluída.\n--------------------")
            return "Remoção concluída."
        else:
            connection.commit()
            connection.close()
            print("Nenhum gasto relacionado ao ID escolhido.\n--------------------")
            return "Nenhum gasto relacionado ao ID escolhido."
    except Exception as e:
        print(f"Erro ao remover gasto:\n{e}\n---------------------------------")
        return False