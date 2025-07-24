from datetime import datetime
import re
import validations

def inputProcesser(input):
    try:
        fields = re.match(r"^(\d+(?:[.,]\d+)?)\s+([a-zA-ZçÇãõáéíóúâêôà]+)(?:\s+(.*))?$", input)
        if not fields:
            print("O usuário inseriu apenas um gasto.")
            return "Os campos obrigatórios não foram preenchidos: VALOR TIPO"
        value, type, rest = fields.groups()
        date = None
        description = None
        if rest:
            date_description = re.match(r"^(\d{1,2}/(?:\d{1,2})?)(?:/\d{4})?\s*(.*)$", rest)
            if date_description:
                date, description = date_description.groups()
                date = validations.checkDate(date)
                if date:
                    date = date.strftime("%Y-%m-%d")
                else:
                    return "Data inválida."
            else:
                description = rest
        if date is None:
            date = validations.checkDate(None)
            date = date.strftime("%Y-%m-%d")
        type = validations.checkType(type)
        value = value.replace(",", ".")
        if type is False:
            return "Tipo inválido!"
        expense = {
            "Value": float(value),
            "Type": type,
            "Date": date,
            "Description": description
        }
        return expense
    except Exception as e:
        print(e)
        return "Algum erro durante o processamento da entrada ocorreu."

def outputProcesser(list):
    output = "---------- Seus Gastos ----------\n"
    for expenseOnList in list:
        Value, Type, Date, Description, ID_Expense = expenseOnList
        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date = Date.strftime("%d/%m/%Y")
        if not Description:
            Description = "Nenhuma"
        output += f"Valor: {Value:.2f}\n"
        output += f"Tipo: {Type}\n"
        output += f"Data: {Date}\n"
        output += f"Descrição: {Description}\n"
        output += "---------------------------------\n"
    return output

def outputProcesserID(list):
    output = "---------- Seus Gastos ----------\n"
    for expenseOnList in list:
        Value, Type, Date, Description, ID_Expense = expenseOnList
        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date = Date.strftime("%d/%m/%Y")
        if not Description:
            Description = "Nenhuma"
        output += f"Valor: {Value:.2f}\n"
        output += f"Tipo: {Type}\n"
        output += f"Data: {Date}\n"
        output += f"Descrição: {Description}\n"
        output += f"ID Para remoção: {ID_Expense}\n"
        output += "---------------------------------\n"
    return output

def filterProcesser(input):
    try:
        filters = {
            "Type": None,
            "Date1": None,
            "Date2": None
        }
        parts = input.split(" ", 2)
        type = validations.checkType(parts[0])
        if type is False:
            date1 = validations.checkDate(parts[0])
        if type:
            filters["Type"] = type
            if len(parts) > 1:
                date1 = validations.checkDate(parts[1])
                if date1:
                    try:
                        date2 = validations.checkDate(parts[2])
                        if date2:
                            if date1 > date2:
                                date1, date2 = date2, date2
                        else: 
                            return "Segunda data inválida."
                        date1 = date1.strftime("%Y-%m-%d")
                        date2 = date2.strftime("%Y-%m-%d")
                        filters["Date1"] = date1
                        filters["Date2"] = date2
                    except IndexError:
                        date1 = date1.strftime("%Y-%m-%d")
                        filters["Date1"] = date1
                else: 
                    return "Primeira data inválida."
        elif date1:
            if len(parts) > 1:
                if date1:
                    try:
                        date2 = validations.checkDate(parts[1])
                        if date2:
                            if date1 > date2:
                                date1, date2 = date2, date2
                        else: 
                            return "Segunda data inválida."
                        date1 = date1.strftime("%Y-%m-%d")
                        date2 = date2.strftime("%Y-%m-%d")
                        filters["Date1"] = date1
                        filters["Date2"] = date2
                    except IndexError:
                        date1 = date1.strftime("%Y-%m-%d")
                        filters["Date1"] = date1
                else: 
                    return "Primeira data inválida."
            elif len(parts) == 1:
                if date1:
                    date1 = date1.strftime("%Y-%m-%d")
                    filters["Date1"] = date1
                else:
                    return "Data inválida."
        else:
            return "Tipo ou Data inválido. Tente novamente."
        print(filters)
        return filters
    except Exception as e:
        print(e)
        return "Algum erro ocorreu durante o processamento do filtro."