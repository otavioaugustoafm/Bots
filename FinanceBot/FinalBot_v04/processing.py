from datetime import datetime
import validations 
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
            match = re.match(r"^(\d{1,2}/\d{1,2}(?:/\d{4})?)(?:\s(.+))?$", rest)
            if match:
                try:
                    date, description = match.groups()
                except:
                    description = None
                    date = match.groups()
                date = validations.checkDate(date)
                if date is None:
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
        output = "\n---------- Seus Gastos ----------\n"
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
            Value = f"{Value:.2f}".replace(".", ",")
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
    
def filtersProcessing(filters):
    print("Processando filtros.\n")
    try:
        date1 = None; date2 = None
        match = re.match(r"^(\d{1,2}/\d{1,2}(?:/\d{4})?)(?:\s(\d{1,2}/\d{1,2}(?:/\d{4})?))?$", filters)
        if match:
            try:
                date1, date2 = match.groups()
                date1 = validations.checkDate(date1)
                date2 = validations.checkDate(date2)
            except:
                date1 = match.groups()
                date1 = validations.checkDate(date1)
            type = None
        else:
            filters = filters.split(" ", 1)
            type = validations.checkType(filters[0])
            if type is None:
                print(f"Processamento finalizado:\n{filters}\n---------------------------------")
                return "Tipo inválido."
            if len(filters) > 1:
                match = re.match(r"^(\d{1,2}/\d{1,2}(?:/\d{4})?)(?:\s(\d{1,2}/\d{1,2}(?:/\d{4})?))?$", filters[1])
                if match:
                    try:    
                        date1, date2 = match.groups()
                        date1 = validations.checkDate(date1)
                        date2 = validations.checkDate(date2)
                        if date1 > date2:
                            date1, date2 = date2, date1
                    except:
                        date1 = match.groups()
                        date1 = validations.checkDate(date1)
        filters = {
            "Type": type,
            "Date1": date1,
            "Date2": date2
        }
        if filters["Type"] is None and filters["Date1"] is None and filters["Date2"] is None:
            filters = "Filtro inválido."
        print(f"Processamento finalizado:\n{filters}\n---------------------------------")
        return filters
    except Exception as e:
        print(f"Erro ao processar os filtros:\n{e}\n---------------------------------")
        return False
    