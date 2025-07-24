from telegram import Update
from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import asyncio
import database
import validations
import inputProcessing

TOKEN = "7541472680:AAFa5GN0m9iI1NBccjfz21hBBj2z287otb4"

GO_TO_FILTERING = 0

GO_TO_SUM = 1

REMOVE = 0

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

async def readFilters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caller = update.message.text
    if caller == "/2":
        await update.message.reply_text("Digite o que quer filtrar no seguinte modelo:\n\nTIPO DATA1 DATA2")
        return GO_TO_FILTERING
    if caller == "/3":
        await update.message.reply_text("Digite o que quer somar no seguinte modelo:\n\nTIPO DATA1 DATA2")
        return GO_TO_SUM
    
async def showFiltered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input = update.message.text
        filters = inputProcessing.filterProcesser(input)
        if isinstance(filters, str):
            await update.message.reply_text(filters)
            return GO_TO_FILTERING
        output = database.showFiltered(filters)
        formatedOutput = inputProcessing.outputProcesser(output)
        if output:
            print("Mostrando gastos filtrados.")
            await update.message.reply_text(formatedOutput)
            return ConversationHandler.END
        else:
            print("Tabela vazia.") 
            await update.message.reply_text("Nenhum gasto encontrado com esses filtros.")
            return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

async def showSum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input = update.message.text
        filters = inputProcessing.filterProcesser(input)
        if isinstance(filters, str):
            await update.message.reply_text(filters)
            return GO_TO_SUM
        output = database.showSum(filters)
        total = output[0] if output and output[0] is not None else 0
        type = filters["Type"] if filters["Type"] is not None else "Todos os tipos."
        if output is None:
            print("Nenhum gasto encontrado para a soma.") 
            await update.message.reply_text("Nenhum gasto encontrado com esses filtros.")
            return ConversationHandler.END
        if filters["Date1"] is not None:
            date1 = datetime.strptime(filters["Date1"], '%Y-%m-%d')
            date1 = date1.strftime("%d/%m/%Y")
        else:
            date1 = "Sem data início."
        if filters["Date2"] is not None:
            date2 = datetime.strptime(filters["Date2"], '%Y-%m-%d')
            date2 = date2.strftime("%d/%m/%Y")
        else:
            date2 = "Sem data final."
        formatedOutput = f"---------------------------------\nTipo: {type}\nDe: {date1}\nAté: {date2}\nTotal: {total:.2f}\n---------------------------------"
        if output:
            print("Mostrando gastos filtrados.")
            await update.message.reply_text(formatedOutput)
            return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

async def readIdToRemove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = database.showAll()
    if output == []:
        await update.message.reply_text("Nenhum gasto encontrado para remover.")
        return ConversationHandler.END
    output = inputProcessing.outputProcesserID(output)
    await update.message.reply_text(output + "Para excluir um gasto, digite o ID correspondente.")
    return REMOVE

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = update.message.text
    true = database.remove(input)
    print(true)
    if true:
        await update.message.reply_text("Gasto removido com sucesso.")
    else:
        await update.message.reply_text("Algum problema ocorreu ao remover o gasto.")
    return ConversationHandler.END
    

def main():
    print("Iniciando o bot...")
    database.createTable()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("0", menu))
    application.add_handler(CommandHandler("1", showAll))
    conv_handler1 = ConversationHandler(
        entry_points = [
            CommandHandler("2", readFilters),
            CommandHandler("3", readFilters) 
        ],
        states = {
            GO_TO_FILTERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, showFiltered)],
            GO_TO_SUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, showSum)]
        },
        fallbacks = []
    )
    conv_handler2 = ConversationHandler(
        entry_points = [CommandHandler("4", readIdToRemove)],
        states = {
            REMOVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove)]
        },
        fallbacks = []
    )
    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling()
    print("Finalizando o bot...")

if __name__ == "__main__":
    main()