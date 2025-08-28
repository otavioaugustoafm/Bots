import re
import validations
from datetime import datetime
import database

def inputProcessing(userInput):
    try:
        currentDate = datetime.strftime(datetime.now().date(), "%Y-%m-%d")
        date = None; description = None
        userInput = userInput.split(" ", 2)
        if len(userInput) == 1:
            print("Apenas um campo foi digitado.")
            return "Apenas um campo foi digitado."
        value = float(userInput[0].replace(",", "."))
        type = validations.checkType(userInput[1])
        if type is None:
            return type
        try:
            match = re.match(r"^(\d{1,2}(?:/)?(?:\d{1,2})?(?:/)?(?:\d+)?)(?:\s(.+))?$", userInput[2])    
            if match:
                try:
                    date, description = match.groups()
                    date = validations.checkDate(date)
                except:
                    date = match.groups()
                    date = validations.checkDate(date)
                    description = None
                if date is None:
                    return "Data inválida."
            else:
                description = userInput[2]
        except:
            date = None
            description = None
        informations = {
            "Value": value,
            "Type": type,
            "Date": date,
            "Description": description
        }
        if date is None:
            informations["Date"] = currentDate
        if description is None:
            informations["Description"] = "Nenhuma"
        return informations
    except Exception as e:
        print(f"Erro ao processar entrada:\n{e}\n--------------------")
        return False

def filterProcessing(userInput):
    try:
        typeList = []
        dateList = []
        recursiveMatch(userInput, typeList, dateList, 1)
        return typeList, dateList
    except Exception as e:
        print(f"Erro ao processar o filtro:\n{e}")
        return False

def monthProcessing(userInput):
    try:
        months = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
        month = userInput.upper()
        if month in months:
            position = months.index(month)
            return position + 1
        else:
            return "Mês inválido."
    except Exception as e:
        print(f"Erro ao processar o mês:\n{e}")

def recursiveMatch(userInput, typeList, dateList, option):
    try:
        if option == 1:
            if userInput is None:
                return
            match = re.match(r"^([a-zA-Z]{1,11})(?:\s(.+))?$", userInput)
            if match:
                type, rest = match.groups()
                type = validations.checkType(type)
                if type:
                    typeList.append(type)
                recursiveMatch(rest, typeList, dateList, 1)
            else:
                recursiveMatch(userInput, typeList, dateList, 2)
        elif option == 2:
            if userInput is None:
                return
            match = re.match(r"^(\d{1,2}(?:/)?(?:\d{1,2})?(?:/)?(?:\d+)?)(?:\s(.+))?$", userInput)
            if match:
                date, rest = match.groups()
                date = validations.checkDate(date)
                if date:
                    dateList.append(date)
                recursiveMatch(rest, typeList, dateList, 2)
    except Exception as e:
        print(f"Erro ao fazer o match recursivo:\n{e}")
        return False
    
def outputProcessing(list):
    try:
        output = "\n---------- Seus Gastos ----------\n"
        for item in list:
            try:
                Id, Value, Type, Date, Description = item
                output += f"ID: {Id}\n"
            except:
                Value, Type, Date, Description = item
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Date = datetime.strftime(Date, '%d/%m/%Y')
            Value = f"{Value:.2f}".replace(".", ",")
            output += f"Valor: R${Value}\n"
            output += f"Tipo: {Type}\n"
            output += f"Data: {Date}\n"
            output += f"Descrição: {Description}"
            output += "\n---------------------------------\n"
        print(output)
        return output
    except Exception as e:
        print(f"Erro ao processar a saída:\n{e}")
        return False, False