from datetime import datetime
import database

def DBdateFormater(date): # formart the date to the DB model
    try: # returns the formated date if sucessful
        date = date.split("/") # splits the date by its '/'
        date = date[2] + "-" + date[1] + "-" + date[0] # formats the date
        return date
    except Exception as e: # returns false if the formatting fails
        print("Algum erro ocorreu durante a transformação da data:\n" + e)
        return False
    
def BRdateFormater(date): # formart the date to BR model
    try: # returns the formated date if sucessful
        date = date.split("-") # splits the date by it's '-'
        date = date[2] + "/" + date[1] + "/" + date[0] # formats the date
        return date
    except Exception as e: # returns false if the formmating fails
        print("Algum erro ocorreu durante a transformação da data:\n" + e)
        return False

def checkType(type): # checks if the type is valid
    print("Checando se o tipo é válido.")
    TYPES = {"TRANSPORTE", "LAZER", "COMPRAS", "ALIMENTAÇÃO", "OUTROS"} # all the types
    if type.upper() in {"ALIMENTACAO", "ALIMENTAÇAO", "ALIMENTACÃO", "ALIMENTAÇÃO"}: # verify the Alimentação issue
        type = "ALIMENTAÇÃO"
    if type.upper() in TYPES: # verify if it's a valid type
        print("O tipo é válido.")
        return type.capitalize()
    else: # returns false if the type is not valid
        print("O tipo não é válido.")
        return False

def checkInput (input): # check the kind of the input the user used
    print("Checando a mensagem do usuário como um todo.")
    input = input.split(" ", 2) # splits the input in 3, if possible
    if len(input) == 1: # checks if the user entered one field
        print("O usuário digitou apenas um campo.")
        return "Entrada inválida! Informe VALOR e TIPO no mínimo.\nExemplo: 29,99 Compras"
    type = checkType(input[1]) # checks if the type is valid
    value = input[0].replace(",", ".") # replaces ',' with '.'
    if type is False: # if type is false, returns a string saying that
        return f"O tipo \"{input[1]}\" não é válido."
    if len(input) == 2: # checks whether the user has entered the minimun number of fields
        print("O usuário digitou dois campos.")
        answer = { 
            "Value": float(value), # gets the value from the user message
            "Type": type, # gets the type from the user message 
            "Date": None,
            "Description": None
        }
        return answer
    elif len(input) == 3: # next lines will check if it is three or four fields 
        aux = input[2].split(" ", 1) # splits the last partition of the input
        aux2 = aux[0].split("/", 2) # splits the first part of the last partition of the input to check if it is a date
        if len(aux) == 1: # if last part its one, it only can be a date or a description with one word
            if len(aux2) == 1: # if splited by it's '/' has lenght 1, means it is not a date
                print("O usuário digitou três campos, sendo DESCRIÇÃO o último e com uma palavra.")
                answer = { 
                    "Value": float(value), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": None,
                    "Description": aux2[0].capitalize() # gets the description from the user message
                }   
            elif len(aux2) == 3: # if splited by it's '/' has lenght '3', means it is a date
                formatedDate = DBdateFormater(aux[0]) # formats the date
                try: # verify if the date format is in the YYYY-MM-DD model
                    datetime.strptime(formatedDate, "%Y-%m-%d") 
                except ValueError:
                    return "A data foi inserida no formato errado."
                print("O usuário digitou três campos, sendo DATA o último")
                answer = { 
                   "Value": float(value), # gets the value from the user message
                   "Type": type, # gets the type from the user message 
                   "Date": formatedDate, # gets the date from the user message
                   "Description": None
                }
            else: # if slited by it's '/' has some other lenght, it means the format is wrong
                return "A data foi inserida no formato errado."          
            return answer
        elif len(aux) == 2: # if the last part of the input has 2 partitions, it can be DATE DESCRIPTION or DESCRIPTION with 2 words
            if len(aux2) == 3: # if the first part of the last partition of the input has lenght 3, it means it is a date - description 
                formatedDate = DBdateFormater(aux[0]) # formats the date
                try: # verify if the date format is in the YYYY-MM-DD model
                    datetime.strptime(formatedDate, "%Y-%m-%d")
                except ValueError:
                    return "A data foi inserida no formato errado."
                print("O usuário digitou os quatro campos.")
                answer = { 
                    "Value": float(value), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": formatedDate, # gets the date from the user message
                    "Description": aux[1].capitalize() # gets the description from the user message
                } 
            else: # if the first part of the last partition of the input has other lenght, it means it is a description - description
                print("O usuário digitou três campos, sendo DESCRIÇÃO o último e com mais de uma palavra.")
                answer = { 
                    "Value": float(value), # gets the value from the user message
                    "Type": type, # gets the type from the user message 
                    "Date": None,
                    "Description": input[2].capitalize() # gets the description from the user message
                }
            return answer

def printExpense(results): # formats the response of the select
    answer = "----- Seus gastos -----\n\n"
    for itemOnList in results: # for each tuple in results, formats a response and adds it to the answer 
        Value, Type, Date, Description = itemOnList
        Date = BRdateFormater(Date) # formats the date to Brazil's model
        if Description is None:
            Description = "Nenhuma"
        answer += f"Valor: {Value:.2f}\n"
        answer += f"Tipo: {Type}\n"
        answer += f"Descrição: {Description}\n"
        answer += f"Data: {Date}\n"
        answer += f"-------------\n"
    return answer # returns the answer ready to be sent to the user