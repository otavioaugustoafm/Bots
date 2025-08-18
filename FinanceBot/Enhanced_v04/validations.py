from datetime import datetime 

def checkDate(date):
    print(f"Verificando data:\n{date}")
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    try:
        date1 = datetime.strptime(date, "%d/%m/%Y").date()
        formatedDate = datetime.strftime(date1, "%Y-%m-%d")
        print(f"{formatedDate}\nData válida.\n--------------------")
        return formatedDate
    except Exception as e:
        try:    
            date2 = f"{date}/{currentYear}"
            date = datetime.strptime(date2, "%d/%m/%Y").date()
            formatedDate = datetime.strftime(date, "%Y-%m-%d")
            print(f"{formatedDate}\nData válida.\n--------------------")
            return formatedDate
        except:
            try:
                date = f"{date}/{currentMonth}/{currentYear}"
                date = datetime.strptime(date, "%d/%m/%Y").date()
                formatedDate = datetime.strftime(date, "%Y-%m-%d")
                print(f"{formatedDate}\nData válida.\n--------------------")
                return formatedDate
            except Exception as e:
                print(f"Data inválida.\n{e}\n--------------------")
                return None
                
def checkType(type):
    print(f"Verificando tipo:\n{type}")
    try:
        TYPES = {"NAMORO", "COMPRAS", "TRANSPORTE", "EXTRA", "COMIDA", "OUTROS"}  
        type = type.upper()
        if type in TYPES:
            type = type.capitalize()
            print(f"Tipo válido.\n--------------------")
            return type
        else:
            type = type.capitalize()
            print(f"Tipo inválido.\n--------------------")
            return None
    except Exception as e:
        print(f"Erro ao checar tipo:\n{e}\n--------------------")
        return False



