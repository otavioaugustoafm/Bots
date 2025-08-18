import asyncio 
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

TOKEN = "7541472680:AAFa5GN0m9iI1NBccjfz21hBBj2z287otb4"



def main():
    application = Application.builder().token(TOKEN).build()
    
    application.run_polling()

if __name__ == "__main__":
    main()