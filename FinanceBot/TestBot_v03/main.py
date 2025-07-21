import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import database
import inputProcessing

TOKEN = "N/A" # bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): # shows the menu
    print("Mostrando o menu.")
    await update.message.reply_text("----------- BOT de Finanças -----------\n\nPara inserir um gasto, apenas digite-o no seguinte modelo:\n\n"
    "VALOR TIPO DATA DESCRIÇÃO\n\nExemplo:\n29,99 Alimentação 26/09/2005 Mercado\n\nOs tipos válidos são: "
    "Transporte - Lazer - Compras - Alimentação - Outros\n\nDigite /1 para mostrar todos os gastos.\n\n"
    "Digite /2 para filtrar os gastos.\n\nDigite /3 para somar os gastos.\n\n")

async def store(update: Update, context: ContextTypes.DEFAULT_TYPE): # stores an expense 
    stringRead = update.message.text # gets the user message
    result = inputProcessing.checkInput(stringRead) # checks the user message - returns a dict or a string
    if isinstance(result, str): # if the result is a string, it reports an error
        await update.message.reply_text(result) 
        return
    result = database.store(result) # if its a dict, it's sent to be stored at the db - returns a string 
    print(result) # result can be a error message or a sucessful operation message
    await update.message.reply_text(result) 

async def showAll(update: Update, context: ContextTypes.DEFAULT_TYPE): # shows the user all date stored
    print("Mostrando todos os dados.")
    results = database.showAll() # calls the select operation on the db - returns a populated or a empty list
    if not results: # if it's not populated, informs the user
        print("Nenhum gasto encontrado.")
        await update.message.reply_text("Nenhum gasto cadastrado até o momento.")
    else: # if it's populated, call the printExpense function - returns the formated message to be sent to the user
        await update.message.reply_text(inputProcessing.printExpense(results))

def main(): # main 
    print("Iniciando o bot...")
    database.createDatabase() # verify if the table already exists or need to be created
    application = Application.builder().token(TOKEN).build() # connect the program with the bot via token
    application.add_handler(CommandHandler("0", start))
    application.add_handler(CommandHandler("1", showAll))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling() # searching for new messages
    print("Finalizando o bot...")

if __name__ == "__main__":
    main()