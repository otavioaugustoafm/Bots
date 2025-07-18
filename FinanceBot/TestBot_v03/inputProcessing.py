from datetime import datetime
import database

def DBdateFormater(date): # formart the date to the DB model
    try:
        print("Transformando data para o modelo do Banco de Dados.")
        date = date.split("/")
        date = date[2] + "-" + date[1] + "-" + date[0]
        print("Data transformada com sucesso.")
        return date
    except:
        print("Algum erro ocorreu durante a transformação da data.")
        return False

def checkType(type): # checks if the type is valid
    print("Checando se o tipo é válido.")
    TYPES = {"TRANSPORTE", "LAZER", "COMPRAS", "ALIMENTAÇÃO", "OUTROS"}
    if type.upper() in {"ALIMENTACAO", "ALIMENTAÇAO", "ALIMENTACÃO", "ALIMENTAÇÃO"}:
        type = "ALIMENTAÇÃO"
    if type.upper() in TYPES:
        print("O tipo é válido.")
        return type.capitalize()
    else:
        print("O tipo não é válido.")
        return False

def checkInput (input): # check how the user made his input
    print("Checando a mensagem do usuário como um todo.")
    input = input.split(" ", 2)
    if len(input) == 1: # checks if the user entered less than two fields
        print("O usuário digitou apenas um campo.")
        return "Entrada inválida! Informe VALOR e TIPO no mínimo.\nExemplo: 29,99 Compras"
    type = checkType(input[1]) # checks if the type is valid
    if type is False:
        return f"O tipo \"{input[1]}\" não é válido."
    if len(input) == 2: # checks whether the user has entered the minimun number of fields
        print("O usuário digitou dois campos.")
        answer = { 
            "Value": float(input[0]), # gets the value from the user message
            "Type": type, # gets the type from the user message 
            "Date": None,
            "Description": "Nenhuma"
        }
        return answer
    elif len(input) == 3: # will check if the user used three or four fields (VALOR TIPO DATA DESCRIÇÃO)
        aux = input[2].split(" ", 1)
        aux2 = aux[0].split("/", 2)
        if len(aux) == 1:
            if len(aux2) == 1:
                print("O usuário digitou três campos, sendo DESCRIÇÃO o último e com uma palavra.")
                answer = { 
                    "Value": float(input[0]), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": None,
                    "Description": aux2[0].capitalize() # gets the description from the user message
                }   
            elif len(aux2) == 3:
                formatedDate = DBdateFormater(aux[0])
                try: 
                    datetime.strptime(formatedDate, "%Y-%m-%d")
                except ValueError:
                    return "A data foi inserida no formato errado."
                print("O usuário digitou três campos, sendo DATA o último")
                answer = { 
                   "Value": float(input[0]), # gets the value from the user message
                   "Type": type, # gets the type from the user message 
                   "Date": formatedDate, # gets the date from the user message
                   "Description": "Nenhuma"
                }
            else:
                return "A data foi inserida no formato errado."          
            return answer
        elif len(aux) == 2:
            if len(aux2) == 3:
                formatedDate = DBdateFormater(aux[0])
                try: 
                    datetime.strptime(formatedDate, "%Y-%m-%d")
                except ValueError:
                    return "A data foi inserida no formato errado."
                print("O usuário digitou os quatro campos.")
                answer = { 
                    "Value": float(input[0]), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": formatedDate, # gets the date from the user message
                    "Description": aux[1].capitalize() # gets the description from the user message
                } 
            else: 
                print("O usuário digitou três campos, sendo descrição o último e com mais de uma palavra.")
                answer = { 
                    "Value": float(input[0]), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": None,
                    "Description": input[2].capitalize() # gets the description from the user message
                }
            return answer
