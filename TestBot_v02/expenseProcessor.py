def checkType(type):
    # all the acceptable types 
    GENERAL_TYPES = ["TRANSPORTE", "LAZER", "ALIMENTAÇÃO", "COMPRAS", "OUTROS"]
    # if the type read from the user message does not correspond with any type in GENERAL_TYPES, return an Error
    if type.upper() in GENERAL_TYPES:
        return True
    else:
        return False

def processExpense(stringRead):
    try:
        # replaces the firt "," for "." and splits the string in three using " " (blank space)
        treated_string = stringRead.replace(",", ".", 1).split(" ", 3)
        # if the list of treated_string has less than two arguments (VALOR TIPO), return an Error
        if len(treated_string) == 1:
            return "Erro: O gasto deve ter, no mínimo, dois campos: VALOR TIPO"
        # try to transform the string on the firt position of the treated_string into a float 
        value = float(treated_string[0])
        if treated_string[1] == "alimentacao" or treated_string[1] == "Alimentacao":
            treated_string[1] = "Alimentação"
        if checkType(treated_string[1]):
            type = treated_string[1].capitalize()
        else: 
            return "Erro: O tipo inserido não é válido. Tente com: Transporte - Lazer - Alimentação - Compras - Outros"
        if len(treated_string) == 3:
            help = treated_string[2]
            if len(help.split("/")) == 3:
                description = "Nenhuma"
                date = treated_string[2]
                formatedDate = date.replace("/", "-")
                formatedDate = formatedDate.split("-")
                formatedDate = formatedDate[2] + "-" + formatedDate[1] + "-" + formatedDate[0]
                bot_answer = {
                    "value": value,
                    "type": type,
                    "description": description,
                    "date": formatedDate
                }
                return bot_answer
            else:    
                description = treated_string[2].capitalize()
        elif len(treated_string) == 2:
            description = "Nenhuma"
        elif len(treated_string) == 4:
            description = treated_string[3].capitalize()
            date = treated_string[2]
            try:
                formatedDate = date.replace("/", "-")
                formatedDate = formatedDate.split("-")
                formatedDate = formatedDate[2] + "-" + formatedDate[1] + "-" + formatedDate[0]
                bot_answer = {
                    "value": value,
                    "type": type,
                    "description": description,
                    "date": formatedDate
                }
                return bot_answer
            except Exception as e:
                print(e)
                return "Erro: A data inserida é inválida. Use o formato: DD/MM/AAAA"    
        bot_answer = {
            "value": value,
            "type": type,
            "description": description
        }
        return bot_answer
    except ValueError:
        return "Erro: Valor digitado no formato errado. Exemplo: 19,99 ou 19.99."
    
if __name__ == "__main__":
    # if we execute this code directly, it uses this exemple below
    answer = processExpense("29,99 Alimentação Almoço na faculdade")
    print(f"----- Gasto registrado! -----\nValor: {answer["value"]:.2f}\nTipo: {answer["type"]}\nDescrição: {answer["description"]}")
