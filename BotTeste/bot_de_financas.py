import asyncio
import ideia
import database
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "N/A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /start"""
    await update.message.reply_text("Olá! Eu sou seu bot de finanças!\nMe envie um gasto no seguinte formato: VALOR TIPO DESCRICAO.\n" \
    "Os tipos podem ser: Transporte - Alimentacao - Lazer - Outros")

async def inserirGasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa a mensagem de texto do usuário que contém o gasto."""
    # Pega o texto da mensagem do Telegram 
    texto_do_usuario = update.message.text 
    # Chama a função do outro arquivo para fazer o trabalho pesado
    resultado = ideia.processarGastos(texto_do_usuario) 
    # Verifica o que a função retornou e envia uma resposta
    if isinstance(resultado, dict):
        # Se o resultado for um dicionário, deu tudo certo
        gasto = resultado
        resposta = (
            "--- Gasto Registrado com Sucesso! ---\n"
            f"Valor: R$ {gasto['valor']:.2f}\n"
            f"Tipo: {gasto['tipo']}\n"
            f"Descricao: {gasto['descricao']}"
        )
        database.salvar_gasto(gasto)
    else:
        # Se não for um dicionário, é uma string de erro que nossa função retornou
        resposta = resultado

    await update.message.reply_text(resposta)
    
async def ver_todos_gastos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca todos os gastos no banco e os envia para o usuário."""
    print("Comando /todosGastos recebido.")
    # Chama a função do banco de dados para buscar os dados
    lista_de_gastos = database.consultar_todos_gastos()

    # Verifica se a lista está vazia
    if not lista_de_gastos:
        await update.message.reply_text("Você ainda não registrou nenhum gasto.")
        return

    # Formata a resposta
    resposta = "--- Seus Gastos Registrados ---\n\n"
    for gasto_tupla in lista_de_gastos:
        # Cada item é uma tupla: (id, valor, tipo, descricao, data)
        gasto_id, valor, tipo, descricao, data = gasto_tupla
        # Trata a descrição caso seja None (nula)
        desc_formatada = descricao if descricao else "(nenhuma)"
        resposta += f"ID: {gasto_id}\n"
        resposta += f"Data: {data}\n"
        resposta += f"Valor: R$ {valor:.2f}\n"
        resposta += f"Tipo: {tipo}\n"
        resposta += f"Descrição: {desc_formatada}\n"
        resposta += "--------------------\n"
    
    # 4. Envia a resposta formatada para o usuário
    await update.message.reply_text(resposta)

async def apagar_todos_gastos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apaga todos os gastos no banco"""
    print("Comando /apagarGastos recebido.")
    # Chama a função do banco de dados para buscar os dados
    database.apagar_todos_gastos()

    await update.message.reply_text("Dados de gastos apagados!")

def main():
    """Inicia o bot."""
    print("Iniciando o bot...")
    database.criar_tabela_gastos()
    application = Application.builder().token(TOKEN).build()

    # Adiciona os "ouvintes" para os comandos e mensagens
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("inserir", inserirGasto))
    application.add_handler(CommandHandler("todosGastos", ver_todos_gastos))
    application.add_handler(CommandHandler("ApagarGastos", apagar_todos_gastos))

    # Liga o bot e o deixa rodando
    application.run_polling()
    print("Bot finalizado.")

if __name__ == '__main__':
    main()