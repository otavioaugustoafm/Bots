from datetime import datetime
import validations 
import processing
import sqlite3
import asyncio
import main

def createDatabase():
    print("---------------------------------\nCriando tabela...\n")
    try:
        connection = sqlite3.connect(r"FinanceBot\Testbot_v04\ExpensesTable.db")
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
        connection = sqlite3.connect(r"FinanceBot\TestBot_v04\ExpensesTable.db")
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
        connection = sqlite3.connect(r"FinanceBot\TestBot_v04\ExpensesTable.db")
        cursor = connection.cursor()
        sqlCommand = "SELECT "
        if input == "/1":
            sqlCommand += "Value, Type, Date, Description "
        elif input == "/3":
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