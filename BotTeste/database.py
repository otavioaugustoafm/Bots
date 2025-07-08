import sqlite3
from datetime import date

NOME_BANCO = "gastos.db"

def criar_tabela_gastos():
    """
    Conecta ao banco de dados e cria a tabela 'gastos' se ela ainda não existir.
    """
    # Conecta ao banco de dados (o arquivo será criado se não existir)
    conn = sqlite3.connect(NOME_BANCO)
    # Cria um 'cursor', que é o objeto que executa os comandos SQL
    cursor = conn.cursor()

    # Executa o comando SQL para criar a tabela
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT,
            data DATE NOT NULL
        );
    """)

    # Confirma a transação e fecha a conexão
    conn.commit()
    conn.close()
    print("Tabela 'gastos' verificada/criada com sucesso.")

def salvar_gasto(gasto_dict):
    """
    Salva um novo gasto no banco de dados.
    """
    try:
        conn = sqlite3.connect(NOME_BANCO)
        cursor = conn.cursor()

        # O comando INSERT. Usamos '?' como placeholders.
        cursor.execute("""
            INSERT INTO gastos (valor, tipo, descricao, data)
            VALUES (?, ?, ?, ?)
        """, (gasto_dict['valor'], gasto_dict['tipo'], gasto_dict['descricao'], date.today()))

        conn.commit()
        conn.close()
        return True # Retorna True se salvou com sucesso
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
        return False # Retorna False se deu algum erro

def consultar_todos_gastos():
    """
    Consulta e retorna todos os gastos registrados no banco de dados.
    """
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    # Executa um SELECT
    cursor.execute("SELECT * FROM gastos ORDER BY data DESC")

    # fetchall() busca todos os resultados e os retorna como uma lista de tuplas
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

def apagar_todos_gastos():
    """
    Consulta e retorna todos os gastos registrados no banco de dados.
    """
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    try:
        # Executa um DELETE
        cursor.execute("DELETE FROM gastos")
        conn.commit()
        conn.close()        

        print("Todos os gastos foram apagados da base de dados.")
        return True
    except Exception as e:
        print(f"Erro ao apagar os gastos: {e}")
        return False