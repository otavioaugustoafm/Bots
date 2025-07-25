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
        print("Mostrando menu.")
        await update.message.reply_text("""---------- Bot de finanças ----------
                                        
        "Insira um gasto: VALOR TIPO DATA DESCRIÇÃO
                                        
        "29,99 Compras 26/09/2005 Camiseta
                                        
        "Digite /1 para mostrar todos os gastos.
                                        
        "Digite /2 para filtrar gastos.
                                        
        "Digite /3 para somar gastos.
                                        
        "Digite /4 para remover um gasto.
                           
        -------------------------------------""")
        return None
    except Exception as e:
        print(e)
        return False

# async def store(update: Update, context: ContextTypes.DEFAULT_TYPE): # VALOR TIPO DATE DESCRIPTION

# async def showAll(update: Update, context: ContextTypes.DEFAULT_TYPE): # /1

# async def showFiltered(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2

# async def showSum(update: Update, context: ContextTypes.DEFAULT_TYPE): # /3

# async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE): # /4