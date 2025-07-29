from datetime import datetime
import validations 
import database
import asyncio
import main
import re

def inputProcessing(input):
    print("Processando entrada...\n")
    try:
        input = input.split(" ", 2)
        if len(input) == 1:
            print("Processamento finalizado:\nApenas um campo foi digitado.\n---------------------------------")
            return "Apenas um campo foi digitado."
        value = input[0].replace(",", "."); type = validations.checkType(input[1]); date = None; description = None
        try:
            value = float(value)
            print(f"Valor: {value}\nValor válido.\n")
        except:
            print(f"Valor: {value}\nValor inválido.\n")
            return "Valor inválido."
        if type is None:
            return "Tipo inválido."
        try:
            rest = input[2]
            match = re.match(r"^(\d{1,2}/(?:\d{1,2}(?:/\d{4})?))?(?:\s(.+))?$", rest)
            if match:
                try:
                    date, description = match.groups()
                except:
                    description = None
                    date = match.groups()
                if validations.checkDate(date) is False:
                    return "Data inválida."
            else:
                date = None
                description = rest
        except:
            date = None
            description = None
        dictionary = {
            "Value": value,
            "Type": type,
            "Date": date,
            "Description": description
        }
        print(f"Processamento finalizado:\n{dictionary}\n---------------------------------")
        return dictionary
    except Exception as e:
        print(f"Erro ao processar gasto:\n{e}\n---------------------------------")
        return "Erro ao processar gasto."

def outputProcessing(list):
    print("Processando saída...")
    try:
        output = "---------- Seus Gastos ----------\n"
        for item in list:
            try:
                Id, Value, Type, Date, Description = item
                output += f"ID: {Id}\n"
            except:
                Value, Type, Date, Description = item
            if Description is None: 
                Description = "Nenhuma"
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Date = datetime.strftime(Date, '%d/%m/%Y')
            Value = str(Value).replace(".", ",")
            output += f"Valor: R${Value}\n"
            output += f"Tipo: {Type}\n"
            output += f"Data: {Date}\n"
            output += f"Descrição: {Description}"
            output += "\n---------------------------------\n"
        print(output)
        return output
    except Exception as e:
        print(f"Erro ao processar a saída:\n{e}\n---------------------------------")
        return False
    