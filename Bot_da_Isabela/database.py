from datetime import datetime
import validations 
import processing
import sqlite3
import asyncio
import main

def createDatabase():
    print("---------------------------------\nCriando tabela...\n")
    try:
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Value REAL NOT NULL,
                Type VARCHAR(11) NOT NULL,
                Date DATETIME,
                Description VARCHAR(255)
            )   
        """)
        connection.commit()
        connection.close()
        print("Tabela criada com sucesso.\n---------------------------------")
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(f"Erro ao criar a tabela de gastos:\n{e}\n---------------------------------")
        return False
    
def store(dict):
    print("Inserindo gasto...\n")
    try:
        Value = dict["Value"]; Type = dict["Type"]; Date = dict["Date"]; Description = dict["Description"]
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        if Date is None:
            Date = datetime.now().date()
        if Description is None:
            Description = "Nenhuma"
        cursor.execute("""
            INSERT INTO Expenses (Value, Type, Date, Description)
            VALUES(?,?,?,?)
        """, (Value, Type, Date, Description))
        connection.commit()
        connection.close()
        print("Gasto armazenado com sucesso.\n---------------------------------")
        return "Gasto armazenado com sucesso."
    except Exception as e:
        print(f"Erro ao inserir gasto:\n{e}\n---------------------------------")
        return False
    
def showAll(input):
    print("Procurando gastos...\n")
    try:
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        sqlCommand = "SELECT "
        if input == "/1":
            sqlCommand += "Value, Type, Date, Description "
        elif input == "/4":
            sqlCommand += "* "
        sqlCommand += "FROM Expenses ORDER BY Date ASC"
        cursor.execute(sqlCommand)
        results = cursor.fetchall()
        connection.close()
        print("Procura concluída.\n---------------------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar todos gastos:\n{e}\n---------------------------------")
        return False
    
def showFiltered(filters):
    print("Procurando gastos filtrados...\n")
    try:
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        type = filters["Type"]; date1 = filters["Date1"]; date2 = filters["Date2"]
        sqlCommand = "SELECT Value, Type, Date, Description FROM Expenses WHERE "
        if type and date1 and date2:
            sqlCommand += "Type = ? AND Date BETWEEN ? AND ?"
            cursor.execute(sqlCommand, [type, date1, date2])
        elif date1 and date2:
            sqlCommand += "Date BETWEEN ? AND ?"
            cursor.execute(sqlCommand, [date1, date2])
        elif type:
            sqlCommand += "Type = ?"
            cursor.execute(sqlCommand, [type,])
        elif date1:
            sqlCommand += "Date = ?"
            cursor.execute(sqlCommand, [date1,])
        results = cursor.fetchall()
        connection.close()
        print("Procura concluída.\n---------------------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar gastos filtrados:\n{e}\n---------------------------------")
        return False
    
def showSum(filters):
    print("Procurando a soma dos gastos filtrados...\n")
    try:
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        type = filters["Type"]; date1 = filters["Date1"]; date2 = filters["Date2"]
        sqlCommand = "SELECT SUM(Value) FROM Expenses WHERE "
        if type and date1 and date2:
            sqlCommand += "Type = ? AND Date BETWEEN ? AND ?"
            cursor.execute(sqlCommand, [type, date1, date2])
        elif date1 and date2:
            sqlCommand += "Date BETWEEN ? AND ?"
            cursor.execute(sqlCommand, [date1, date2])
        elif type:
            sqlCommand += "Type = ?"
            cursor.execute(sqlCommand, [type,])
        elif date1:
            sqlCommand += "Date = ?"
            cursor.execute(sqlCommand, [date1,])
        results = cursor.fetchone()
        connection.close()
        print("Procura concluída.\n---------------------------------")
        return results
    except Exception as e:
        print(f"Erro ao mostrar gastos filtrados:\n{e}\n---------------------------------")
        return False
    
def remove(id):
    print("Realizando remoção de gasto...\n")
    try:
        connection = sqlite3.connect(r"Bot_da_Isabela\ExpensesTable.db")
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM Expenses 
            WHERE ID = ?
        """,(id,))
        deleted = cursor.rowcount
        if deleted > 0:
            print("Remoção concluída.\n---------------------------------")
            connection.commit()
            connection.close()
            return "Remoção concluída."
        else:
            print("Operação concluída: Nada removido.\n---------------------------------")
            connection.commit()
            connection.close()
            return "Nenhum gasto relacionado ao ID escolhido."
    except Exception as e:
        print(f"Erro ao remover gasto:\n{e}\n---------------------------------")
        return False
    
    