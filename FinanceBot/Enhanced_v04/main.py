from telegram.ext import Application, ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from datetime import datetime
from telegram import Update
import processing
import database

TOKEN = "N/A"

GO_TO_FILTERING, GO_TO_SUM, GO_TO_REMOVE, GO_TO_MONTH = range(4)

async def showMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Mostrando menu.\n---------------------------------")
        await update.message.reply_text("---------- Bot de finanças ----------\nInsira um gasto no seguinte modelo:\n\n VALOR TIPO DATA DESCRIÇÃO\n29,99 Compras 26/09/2005 Camiseta\n\nOs tipos disponíveis são: Namoro, Transporte, Comida, Compras, Extra e Outros.\n\nDigite /1 mostrar os gastos e a soma deles em um mês.\n\nDigite /2 para filtrar gastos.\n\nDigite /3 para somar gastos.\n\nDigite /4 para remover um gasto.\n\nDigite /5 para mostrar todos os gastos.\n-------------------------------------")
        return True
    except Exception as e:
        print(e)
        return False

async def store(update: Update, context: ContextTypes.DEFAULT_TYPE): # VALOR TIPO DATE DESCRIPTION
    try:
        input = update.message.text
        input = processing.inputProcessing(input)
        if input is False:
            await update.message.reply_text("Entrada inválida.")
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
        try:
            await update.message.reply_text(output)
        except:
            await update.message.reply_text("A quantidade de gastos ultrapassa o limite de tamanho da mensagem, infelizmente não é possível mostrá-los todos.\n\nUtilize a função /1 para filtrar por mês.")
    except Exception as e:
        print(e)
        return False
    
async def readInput(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2 /3 /4
    try:
        input = update.message.text
        if input == "/2":
            await update.message.reply_text("-----------------------------------------\nDigite os TIPOS que deseja filtrar separados por espaço\n\nSe desejar, insira a DATA ou PERÍODO\n\nExemplo:\nExtra Transporte 26/09/2025 20/10/2025\n-----------------------------------------")
            return GO_TO_FILTERING
        elif input == "/3":
            await update.message.reply_text("-----------------------------------------\nDigite os TIPOS que deseja somar separados por espaço\n\nSe desejar, insira a DATA ou PERÍODO\n\nExemplo:\nExtra Transporte 26/09/2025 20/10/2025\n-----------------------------------------")
            return GO_TO_SUM
        elif input == "/4":
            output = database.showAll(input)
            if output == []:
                await update.message.reply_text("Nenhum gasto registrado até o momento.")
                return
            output = processing.outputProcessing(output)
            await update.message.reply_text(f"{output}\nSelecione o ID do gasto que você quer apagar.")
            return GO_TO_REMOVE
        elif input == "/1":
            await update.message.reply_text(f"Qual mês quer buscar os gastos essenciais?")
            return GO_TO_MONTH
    except Exception as e:
        print(e)
        return False
    
async def showFiltered(update: Update, context: ContextTypes.DEFAULT_TYPE): # /2
    try:   
        input = update.message.text
        types, dates = processing.filterProcessing(input)
        if types is False:
            await update.message.reply_text("Erro ao mostrar gastos filtrados")
            return ConversationHandler.END
        output = database.showFiltered(types, dates)
        if output == []:
            await update.message.reply_text("Nenhum gasto registrado com esses filtros até o momento.")
            return ConversationHandler.END
        elif output is False:
            await update.message.reply_text("Algum erro ocorreu na busca no banco de dados.")
            return ConversationHandler.END
        output = processing.outputProcessing(output)
        try:
            await update.message.reply_text(output)
        except:
            await update.message.reply_text("A quantidade de gastos ultrapassa o limite de tamanho da mensagem, infelizmente não é possível mostrá-los todos.\n\nTente filtrar mais utilizando outros filtros ou utilize a função /1 para filtrar por mês, porém sem filtros.")
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

async def showSum(update: Update, context: ContextTypes.DEFAULT_TYPE): # /3
    try:   
        input = update.message.text
        types, dates = processing.filterProcessing(input)
        if types is False:
            await update.message.reply_text("Erro ao mostrar gastos filtrados")
            return ConversationHandler.END
        sum = database.showSum(types, dates)
        if sum[0] is None:
            await update.message.reply_text("Nenhum gasto encontrado com esses filtros.")
            return ConversationHandler.END
        elif sum is False:
            await update.message.reply_text("Algum erro ocorreu na busca no banco de dados.")
            return ConversationHandler.END
        
        sum = f"{sum[0]:.2f}".replace(".", ",")
        output = f"R${sum}"
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

async def showMonth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:   
        input = update.message.text
        month = processing.monthProcessing(input)
        if isinstance(month, str):
            await update.message.reply_text("Mês Inválido. Tente novamente:")
            return GO_TO_MONTH
        currentYear = datetime.now().year
        date = f"4/{month}/{currentYear}"
        nextDate = '3/'
        if month == 12:
            nextDate += f"1/{currentYear}"
        else:
            nextDate += f"{month + 1}/{currentYear}"
        date = datetime.strptime(date, "%d/%m/%Y").date()
        date = datetime.strftime(date, "%Y-%m-%d")
        nextDate = datetime.strptime(nextDate, "%d/%m/%Y").date()
        nextDate = datetime.strftime(nextDate, "%Y-%m-%d")
        results1, sum1, results2, sum2 = database.showMonth(date, nextDate)
        print(results1)
        if results1 == [] and results2 == []:
            await update.message.reply_text("Nenhum gasto nesse mês.")
            return ConversationHandler.END
        try: 
            output = "Gastos Gerais:\n"
            output += processing.outputProcessing(results1)
            output += "Gastos Extras:\n\n"
            output += processing.outputProcessing(results2)
            if sum1[0] is None:
                output += f"\nNada relacionado aos tipos gerais nesse mês.\n---------------------------------"
            else:
                output += f"\nSoma dos Gastos Gerais: R${sum1[0]}\n---------------------------------".replace(".", ",")
            if sum2[0] is None:
                output += f"\nNada relacionado ao tipo Extra nesse mês.\n---------------------------------"
            else:
                output += f"\nSoma dos Gastos Extras: R${sum2[0]}\n---------------------------------".replace(".", ",")
            sum = sum1[0] + sum2[0]
            sum = f"{sum:.2f}"
            output += f"\nSoma total dos gastos: R${sum}\n---------------------------------".replace(".", ",")
            await update.message.reply_text(output)
        except:
            output = "Gastos Gerais:\n"
            output += processing.outputProcessing(results1)
            await update.message.reply_text(output)
            output = "Gastos Extras:\n\n"
            output += processing.outputProcessing(results2)
            if sum1[0] is None:
                output += f"\nNada relacionado aos tipos gerais nesse mês.\n---------------------------------"
            else:
                output += f"\nSoma dos Gastos Gerais: R${sum1[0]}\n---------------------------------".replace(".", ",")
            if sum2[0] is None:
                output += f"\nNada relacionado ao tipo Extra nesse mês.\n---------------------------------"
            else:
                output += f"\nSoma dos Gastos Extras: R${sum2[0]}\n---------------------------------".replace(".", ",")
            sum = sum1[0] + sum2[0]
            sum = f"{sum:.2f}"
            output += f"\nSoma total dos gastos: R${sum}\n---------------------------------\n".replace(".", ",")
            await update.message.reply_text(output)
        return ConversationHandler.END
    except Exception as e:
        print(e)
        return ConversationHandler.END

def main():
    database.createTable()
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points = [
            CommandHandler("2", readInput),
            CommandHandler("3", readInput),
            CommandHandler("4", readInput),
            CommandHandler("1", readInput)
            ],
        states = {
            GO_TO_FILTERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, showFiltered)],
            GO_TO_SUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, showSum)],
            GO_TO_REMOVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove)],
            GO_TO_MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, showMonth)]
            },
        fallbacks = []
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", showMenu))
    application.add_handler(CommandHandler("5", showAll))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store))
    application.run_polling()

if __name__ == "__main__":
    main()        
