import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import expenseProcessor
import database

TOKEN = "N/A"

READTYPE = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # waits for the network confirmation and sends the following message
    await update.message.reply_text("---------- Bot de Finanças ----------\n\n"\
    "Escolha entre os seguintes tipos: Transporte - Lazer - Alimentação - Compras - Outros\n\n" \
    "Envie dados no modelo: VALOR TIPO DESCRIÇÃO\n\nDigite /1 para mostrar TODOS os gastos.\n\nDigite /2 para exibir todos os gastos filtrados por tipo")

async def storeExpense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # stringRead receives the user message
    stringRead = update.message.text
    # calls the processExpense function from expenseProcesor.py. FunctionReturn receives the return from procesExpense 
    functionReturn = expenseProcessor.processExpense(stringRead)
    # if processExpense returns a dict type answer, store the data. 
    if isinstance(functionReturn, dict):
        if database.storeData(functionReturn):
            await update.message.reply_text("Gasto armazenado com sucesso")
        else:
            await update.message.reply_text("Algum erro ocorreu. Tente novamente.")
    # if processExpense returns a string type answer, show the user the string error
        print("Inserção de dados feita.")
    else: 
        await update.message.reply_text(functionReturn)

async def showAllData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # uses the shoAllData function to retrieve all tuples of the table
        results = database.showAllData()
        # if showAllData returned False, it is because the table is empty
        if not results:
            await update.message.reply_text("Não há nenhum gasto cadastrado até o momento")
        else:
            answer = "----- Seus gastos -----\n\n"
            # for each itemOnList, it formats a message
            for itemOnList in results:
                value, type, description, date = itemOnList
                dateFormat = date.split("-")
                date = dateFormat[2] + "/" + dateFormat[1] + "/" + dateFormat[0]
                answer += f"Valor: {value}\n"
                answer += f"Tipo: {type}\n"
                answer += f"Description: {description}\n"
                answer += f"Data: {date}\n"
                answer += f"-------------\n"
            await update.message.reply_text(answer)
            print("Monstrando todos os dados.")
    except Exception as e:
        await update.message.reply_text("Erro ao mostrar todos os gastos")

async def readFilter(update, context):
    await update.message.reply_text("Digite o que quer filtrar:\n\nPara período: DD/MM/AAAA\n\nPara tipo digite algum entre: Transporte - Lazer - Alimentação - Compras - Outros")
    return READTYPE

async def filterByType (update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # checks if is a acceptable type
        stringRead = update.message.text
        if stringRead == "alimentacao" or stringRead == "Alimentacao":
            stringRead = "Alimentação"
        if expenseProcessor.checkType(stringRead):
            # gathers the expenses for the type
            results = database.filterByType(stringRead)
            # checks if the results has at least one expense
            if not results:
                await update.message.reply_text(f"Não há nenhum gasto cadastrado a {stringRead} até o momento")
                return ConversationHandler.END
            answer = "----- Seus gastos -----\n\n"
            # for each itemOnList, it formats a message
            for itemOnList in results:
                value, type, description, date = itemOnList
                answer += f"Valor: {value}\n"
                answer += f"Tipo: {type}\n"
                answer += f"Description: {description}\n"
                answer += f"Data: {date}\n"
                answer += f"-------------\n"
            await update.message.reply_text(answer)
            return ConversationHandler.END
        else:
            await update.message.reply_text("O tipo digitado é inválido. Digite /2 e tente novamente.")
            return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text("Erro ao mostrar gastos filtrados por tipo")
        return ConversationHandler.END
        
def main():
    print("Iniciando o bot...")
    database.createDataBase()
    application = Application.builder().token(TOKEN).build()
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler("2", readFilter)],
        states={
            READTYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, filterByType)]
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler1)
    application.add_handler(CommandHandler("0", start))
    application.add_handler(CommandHandler("1", showAllData))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, storeExpense))
    application.run_polling()
    print("Bot finalizado.")

if __name__ == '__main__':
    main()