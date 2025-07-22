import re
import validations

def inputProcesser(input):
    try:
        fields = re.match(r"^(\d+(?:[.,]\d+)?)\s+([a-zA-ZçÇãõáéíóúâêôà]+)(?:\s+(\d{1,2}/\d{1,2}(?:/\d{4})?))?(?:\s+(.*))?$", input)
        if fields:
            fields = fields.groups()
        else:
            return "Os campos obrigatórios não foram preenchidos: VALOR TIPO."
        value = fields[0].replace(",", ".")
        type = validations.checkType(fields[1])
        date = validations.checkDate(fields[2])
        description = fields[3]
        if type is False:
            return "Tipo inválido!"
        elif date is False:
            return "Data inválida!"
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
