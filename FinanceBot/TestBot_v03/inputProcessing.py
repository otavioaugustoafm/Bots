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
        Value, Type, Date, Description = expenseOnList
        Date = datetime.strptime(Date, "%Y-%m-%d")
        Date = Date.strftime("%d/%m/%Y")
        if not Description:
            Description = "Nenhuma"
        print(Description)
        output += f"Valor: {Value:.2f}\n"
        output += f"Tipo: {Type}\n"
        output += f"Data: {Date}\n"
        output += f"Descrição: {Description}\n"
        output += "---------------------------------\n"
    return output