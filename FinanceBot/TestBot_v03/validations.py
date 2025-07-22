from datetime import datetime

def checkType(type):
    try:
        TYPES = {"COMPRAS", "ALIMENTAÇÃO", "TRANSPORTE", "OUTROS"}
        if type.upper() in {"ALIMENTACAO", "ALIMENTAÇAO", "ALIMENTACÃO"}:
            type = "Alimentação"
        if type.upper() in TYPES:
            print("Tipo válido.")
            return type.capitalize()
        else:
            print("Tipo inválido.")
            return False
    except Exception as e:
        print(e)
        return False

def checkDate(date):
    if date is None:
        return datetime.now().date()
    try:
        formatedDate = datetime.strptime(date, '%d/%m/%Y')
        formatedDate = formatedDate.date()
        print("Data válida. (Com ano)")
        return formatedDate
    except ValueError:
        try:
            formatedDate = datetime.strptime(date, '%d/%m')
            formatedDate = formatedDate.date()
            formatedDate = formatedDate.replace(year = datetime.now().year)
            print("Data válida. (Sem ano)")
            return formatedDate 
        except ValueError:
            print("Data inválida.")
            return None
        