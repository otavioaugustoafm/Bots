from datetime import datetime
import processing
import database
import asyncio
import main

def checkType(type): # Type -> String
    try:
        TYPES = {"ALIMENTAÇÃO", "TRANSPORTE", "COMPRAS", "OUTROS"}
        if type.upper in {"ALIMENTACAO", "ALIMENTAÇAO", "ALIMENTACÃO"}:
            type == "ALIMENTAÇÃO"
        if type.upper in TYPES:
            print("Tipo válido.")
            return type.capitalize()
        else:
            print("Tipo inválido.")
            return None
    except Exception as e:
        print(e)
        return False
    
def checkDate(date): # Date -> String
    print(date)
    try:
        date = datetime.strptime(date, '%d/%m/%Y').date()
        date = datetime.strftime(date, '%Y-%m-%d')
        print("Data válida. (Com ano)")
        print(date)
        return date
    except Exception as e:
        try:
            currentYear = datetime.now().year
            stringDate = f"{date}/{currentYear}"
            date = datetime.strptime(stringDate, '%d/%m/%Y')
            date = datetime.strftime(date, '%Y-%m-%d')
            print("Data válida. (Sem ano)")
            print(date)
            return date
        except Exception as e:
            print("Data inválida")
            return False