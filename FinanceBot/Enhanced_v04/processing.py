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
            return None
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
        print(f"Erro ao processar entrada:\n{e}")
        return False

def filterProcessing(userInput):
    try:
        list = []
        recursiveMatch(userInput, list, 1)
        return list

    except Exception as e:
        print(f"Erro ao processar o filtro:\n{e}")
        return False


def recursiveMatch(userInput, list, option):
    try:
        if option == 1:
            match = re.match(r"^([a-zA-Z]{1,11})(?:\s(.+))?$", userInput)
            if match:
                try:
                    type, rest = match.groups()
                    type = validations.checkType(type)
                    if type:
                        list.append(type)
                    recursiveMatch(rest, list, 1)
                except:
                    type = match.groups()
                    type = validations.checkType(type)
                    if type:
                        list.append(type)
                    list.append(type)
                    return
            else:
                print(f"fui procurar um numero e encontrei {userInput}")
        #elif option == 2:
    except Exception as e:
        print(f"Erro ao fazer o match recursivo:\n{e}")
        return False

if __name__ == "__main__":
    a = filterProcessing("Extra Namoro Transporte")
    print(a)