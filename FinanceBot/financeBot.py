import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import expenseProcessor
import database

TOKEN = "N\A"

READTYPE = 0

READDATE = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # waits for the network confirmation and sends the following message
    await update.message.reply_text("---------- Bot de Finanças ----------\n\n"\
    "Para adicionar os dados de um gasto, apenas digite no seguinte modelo: VALOR TIPO DESCRIÇÃO\nExemplo: 29,99 Alimentação Descrição\n\n" \
    "Os tipos disponíveis são: Transporte - Lazer - Alimentação - Compras - Outros\n\n" \
    "Digite /1 para mostrar TODOS os gastos.\n\nDigite /2 para exibir todos os gastos filtrados por tipo\n\nDigite /3 para exibir todos os gastos filtrados por data ou período\n\n")

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

async def readFilterType(update, context):
    await update.message.reply_text("Digite o tipo que quer filtrar:\nOs tipos disponíveis são: Transporte - Lazer - Alimentação - Compras - Outros")
    return READTYPE

async def readFilterDate(update, context):
    await update.message.reply_text("Digite a data ou período que quer filtrar:\nData: DD/MM/AAAA\nPeríodo: DD/MM/AAAA a DD/MM/AAAA")
    return READDATE

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
    
async def filterByDate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stringRead = update.message.text
        stringRead = stringRead.split(" a ")
        if len(stringRead) == 1:
            stringFormat = stringRead[0]
            stringFormat = stringFormat.split("/")
            formatedDate = stringFormat[2] + "-" + stringFormat[1] + "-" + stringFormat[0]
            results = database.filterByDate(formatedDate)
        elif len(stringRead) == 3:
            stringFormat = stringRead[0]
            stringFormat = stringFormat.split("/")
            formatedDate = stringFormat[2] + "-" + stringFormat[1] + "-" + stringFormat[0]
            stringFormat = stringRead[1]
            stringFormat = stringFormat.split("/")
            aux = stringFormat[2] + "-" + stringFormat[1] + "-" + stringFormat[0]
            formatedDate += " " + aux
            results = database.filterByData(formatedDate)
        if not results:
            await update.message.reply_text("Nenhum gasto cadastrado nessa data ou período.")
        elif results is False:
            await update.message.reply_text("Erro ao filtrar por data.")
        answer = "----- Seus gastos -----\n\n"
        for itemOnList in results:
            value, type, description, date = itemOnList
            answer += f"Valor: {value}\n"
            answer += f"Tipo: {type}\n"
            answer += f"Description: {description}\n"
            answer += f"Data: {date}\n"
            answer += f"-------------\n"
        await update.message.reply_text(answer)
        return ConversationHandler.END
    except Exception as e:
        print(e)
        await update.message.reply_text("Erro ao filtrar por data ou período")
        return ConversationHandler.END
    
def main():
    print("Iniciando o bot...")
    database.createDataBase()
    application = Application.builder().token(TOKEN).build()
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler("2", readFilterType)],
        states={
            READTYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, filterByType)]
        },
        fallbacks=[]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("3", readFilterDate)],
        states={
            READDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, filterByDate)]
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    application.add_handler(CommandHandler("0", start))
    application.add_handler(CommandHandler("1", showAllData))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, storeExpense))
    application.run_polling()
    print("Bot finalizado.")

if __name__ == '__main__':
    main()