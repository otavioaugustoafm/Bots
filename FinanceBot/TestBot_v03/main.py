from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import asyncio
import database
import inputProcessing

TOKEN = "N/A"

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("---------- Bot de Finanças ----------\n\nInsira os dados do seu gasto enviando uma " \
    "mensagem no seguinte modelo:\n\nVALOR TIPO DATA DESCRIÇÃO\n299,99 Compras 26/09/2005 Calça\n\nDigite /1 " \
    "para mostrar todos os gastos.\n\nDigite /2 para filtrar.\n\nDigite /3 para somar gastos.")

async def store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Inserindo gasto...")
    try:
        input = inputProcessing.inputProcesser(update.message.text)
        if isinstance(input, str):
            await update.message.reply_text(input)
        elif database.store(input):
            await update.message.reply_text("Gasto armazenado com sucesso.")
        else:
            await update.message.reply_text("Algum erro ocorreu ao armazenar o gasto.")
    except Exception as e:
        print(e)

async def showAll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        output = database.showAll()
        if output:
            output = inputProcessing.outputProcesser(output)
            print("Mostrando gastos.")
            await update.message.reply_text(output)
        else:
            print("Tabela vazia.") 
            await update.message.reply_text("Nenhum gasto foi cadastrado até o momento.")
    except Exception as e:
        print(e)

def main():
    print("Iniciando o bot...")
    database.createTable()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("0", menu))
    application.add_handler(CommandHandler("1", showAll))
    #application.add_handler(CommandHandler("2", showFiltered))
    #application.add_handler(CommandHandler("3", showSum))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling()
    print("Finalizando o bot...")


if __name__ == "__main__":
    main()