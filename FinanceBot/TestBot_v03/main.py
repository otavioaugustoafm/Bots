import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import database
import inputProcessing

TOKEN = "N/A" # bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Mostrando o menu.")
    await update.message.reply_text("----- BOT de Finanças -----\n\nPara inserir um gasto, apenas digite-o.\n\n"
    "Use o formato: VALOR TIPO DATA DESCRIÇÃO\nExemplo: 29,99 Alimentação 01/12/2020 Mercado\n\nOs tipos válidos são: "
    "\"TRANSPORTE\", \"LAZER\", \"COMPRAS\", \"ALIMENTAÇÃO\", \"OUTROS\"\n\nDigite /0 para mostrar o menu novamente.\n\nDigite /1 para mostrar TODOS os gastos.\n\n"
    "Digite /2 para filtrar os gastos.\n\nDigite /3 para somar os gastos.\n\n")

async def readFilters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text 

if __name__ == "__main__":
    print("Iniciando o bot...")
    database.createDatabase()
    start()
    application = Application.builder().token(TOKEN).build()
