from telegram.ext import Application, ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update
import validations 
import processing
import database
import asyncio

TOKEN = "N/A"

SHOW_ALL, SHOW_FILTERED, SHOW_SUM = range(3)

async def showMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Mostrando menu.\n")
        await update.message.reply_text("---------- Bot de finanças ----------\nInsira um gasto: VALOR TIPO DATA DESCRIÇÃO\n29,99 Compras 26/09/2005 Camiseta\n\nDigite /1 para mostrar todos os gastos.\n\nDigite /2 para filtrar gastos.\n\nDigite /3 para somar gastos.\n\nDigite /4 para remover um gasto.\n-------------------------------------")
        return True
    except Exception as e:
        print(e)
        return False

async def store(update: Update, context: ContextTypes.DEFAULT_TYPE): # VALOR TIPO DATE DESCRIPTION
    try:
        input = update.message.text
        input = processing.inputProcessing(input)
        if isinstance(input, str):
            await update.message.reply_text(input)
            return
        output = database.store(input)
        await update.message.reply_text(output)
    except Exception as e:
        print(e)
        return False
    
async def showAll(update: Update, context: ContextTypes.DEFAULT_TYPE): # /1
    try:
        output = database.showAll(update.message.text)
        if output == []:
            await update.message.reply_text("Nenhum gasto registrado até o momento.")
            return
        output = processing.outputProcessing(output)
        await update.message.reply_text(output)
    except Exception as e:
        print(e)
        return False

# async def showFiltered(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2

# async def showSum(update: Update, context: ContextTypes.DEFAULT_TYPE): # /3

# async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE): # /4

def main():
    database.createDatabase()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", showMenu))
    application.add_handler(CommandHandler("1", showAll))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling()

if __name__ == "__main__":
    main()        
