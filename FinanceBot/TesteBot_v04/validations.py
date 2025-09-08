from datetime import datetime

def checkType(type): # Type is a String
    try:
        TYPES = {"ALIMENTAÇÃO", "TRANSPORTE","NAMORO", "COMPRAS", "MENSAL", "EXTRA", "OUTROS"}
        if type.upper() in {"ALIMENTACAO", "ALIMENTAÇAO", "ALIMENTACÃO"}:
            type = "ALIMENTAÇÃO"
        if type.upper() in TYPES:
            type = type.capitalize()
            print(f"Tipo: {type}\nTipo válido.\n")
            return type
        else:
            print(f"Tipo: {type}\nTipo inválido.\n")
            return None
    except Exception as e:
        print(e)
        return False
    
def checkDate(date): # Date is a String
    print(f"Data: {date}")
    try:
        date = datetime.strptime(date, '%d/%m/%Y').date()
        date = datetime.strftime(date, '%Y-%m-%d')
        print("Data válida. (Com ano)\n")
        return date
    except:
        try:
            currentYear = datetime.now().year
            stringDate = f"{date}/{currentYear}"
            date = datetime.strptime(stringDate, '%d/%m/%Y')
            date = datetime.strftime(date, '%Y-%m-%d')
            print("Data válida. (Sem ano)\n")
            return date
        except:
            print("Data inválida\n")
            return None