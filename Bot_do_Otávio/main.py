from telegram.ext import Application, ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update
import validations 
import processing
import database
import asyncio

TOKEN = "8030257844:AAEzUlXSamdDxZHqA1tnSSk9zMc9fpSWEbA"

GO_TO_FILTERING, GO_TO_SUM, GO_TO_REMOVE = range(3)

async def showMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Mostrando menu.\n---------------------------------")
        await update.message.reply_text("---------- Bot de finanças ----------\nInsira um gasto no seguinte modelo:\n\n VALOR TIPO DATA DESCRIÇÃO\n29,99 Compras 26/09/2005 Camiseta\n\nDigite /1 para mostrar todos os gastos.\n\nDigite /2 para filtrar gastos.\n\nDigite /3 para somar gastos.\n\nDigite /4 para remover um gasto.\n-------------------------------------")
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
    
async def readInput(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2 /3 /4
    try:
        input = update.message.text
        if input == "/2":
            await update.message.reply_text("Digite como quer filtrar a exibição dos gastos.\n\nExemplos:\n\nTipo e Período:\nTIPO DATA1 DATA2\n\nTipo e Data:\nTIPO DATA\n\nPeríodo:\nDATA1 DATA2\n\nTipo:\nTIPO\n\nData:\nDATA\n\n")
            return GO_TO_FILTERING
        elif input == "/3":
            await update.message.reply_text("Digite como quer filtrar a soma.\n\nExemplos:\n\nTipo e Período:\nTIPO DATA1 DATA2\n\nTipo e Data:\nTIPO DATA\n\nPeríodo:\nDATA1 DATA2\n\nTipo:\nTIPO\n\nData:\nDATA\n\n")
            return GO_TO_SUM
        elif input == "/4":
            output = database.showAll(input)
            if output == []:
                await update.message.reply_text("Nenhum gasto registrado até o momento.")
                return
            output = processing.outputProcessing(output)
            await update.message.reply_text(f"{output}\nSelecione o ID do gasto que você quer apagar.")
            return GO_TO_REMOVE
    except Exception as e:
        print(e)
        return False
    
async def showFiltered(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2
    try:   
        input = update.message.text
        filters = processing.filtersProcessing(input)
        if isinstance(filters, str):
            await update.message.reply_text(filters)
            return ConversationHandler.END
        output = database.showFiltered(filters)
        if output == []:
            await update.message.reply_text("Nenhum gasto registrado com esses filtros até o momento.")
            return ConversationHandler.END
        elif output is False:
            await update.message.reply_text("Algum erro ocorreu na busca no banco de dados.")
            return ConversationHandler.END
        output = processing.outputProcessing(output)
        await update.message.reply_text(output)
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

async def showSum(update: Update, context: ContextTypes.DEFAULT_TYPE): # /3
    try:   
        input = update.message.text
        filters = processing.filtersProcessing(input)
        if isinstance(filters, str):
            await update.message.reply_text(filters)
            return ConversationHandler.END
        sum = database.showSum(filters)
        if sum[0] is None:
            await update.message.reply_text("Nenhum gasto encontrado com esses filtros.")
            return ConversationHandler.END
        elif sum is False:
            await update.message.reply_text("Algum erro ocorreu na busca no banco de dados.")
            return ConversationHandler.END
        sum = f"{sum[0]:.2f}".replace(".")
        output = f"--------- Soma dos Gastos ---------\nTipo: {filters["Type"]}\nDe: {filters["Date1"]}\nAté: {filters["Date2"]}\nSoma: R${sum[0]:.2f}\n---------------------------------"
        await update.message.reply_text(output)
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE): # /4
    try:
        input = update.message.text
        output = database.remove(input)
        await update.message.reply_text(output)
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

def main():
    database.createDatabase()
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points = [
            CommandHandler("2", readInput),
            CommandHandler("3", readInput),
            CommandHandler("4", readInput)
            ],
        states = {
            GO_TO_FILTERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, showFiltered)],
            GO_TO_SUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, showSum)],
            GO_TO_REMOVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove)]
            },
        fallbacks = []
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", showMenu))
    application.add_handler(CommandHandler("1", showAll))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling()

if __name__ == "__main__":
    main()        
