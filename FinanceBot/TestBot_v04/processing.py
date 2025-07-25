import validations 
import database
import asyncio
import main
import re

def inputProcessing(input):
    input = input.split(" ", 2)
    value = input[0]; type = input[1]; rest = input[2]
    rest = re.match(r"(\d{1,2}/\d{1,2}(?:/\d{4})?)(?:\s.*)?", input)
    if rest:
        try:
            date, description = rest.groups()
        except Exception as e:
            date = rest.groups()

if __name__ == "__main__":
    inputProcessing("29,99 Compras 10/10/2005")