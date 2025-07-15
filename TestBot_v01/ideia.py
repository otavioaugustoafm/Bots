def confereTipo(tipo):
    TIPOS_VALIDOS = ["TRANSPORTE", "ALIMENTACAO", "LAZER", "OUTROS"]
    if tipo.upper() in TIPOS_VALIDOS:
        return True
    else:
        return False


def processarGastos(message):
    # stringGasto = input() <- Caso queira rodar localmente
    stringGasto_tratada = message.replace(",", ".", 1).split(" ", 2)
    try:
        if len(stringGasto_tratada) < 2:
            # print("Erro: Formato inválido. É preciso no mínimo 'Valor Tipo'.") <- Caso queira rodar localmente
            # return None <- Caso queira rodar localmente
            return "Erro: Formato inválido. É preciso no mínimo VALOR e TIPO."
        valor_str = stringGasto_tratada[0]
        tipo = stringGasto_tratada[1]
        valor = float(valor_str)
        if not confereTipo(tipo):
            # print(f"Erro: O tipo inserido não é válido. Use: Transporte - Alimentacao - Lazer - Outros.") <- Caso queira rodar localmente
            # return None <- Caso queira rodar localmente
            return "Erro: O tipo inserido não é válido. Use: Transporte - Alimentacao - Lazer - Outros."
        if len(stringGasto_tratada) < 3:
            descricao = None
        else:
            descricao = stringGasto_tratada[2]
        dados_processados = {
            "valor": valor,
            "tipo": tipo,
            "descricao": descricao
        }
        return dados_processados
    except ValueError:
        # print(f"Erro: O valor '{valor_str}' não é um número válido.") <- Caso queira rodar localmente
        # return None <- Caso queira rodar localmente
        return "Erro: O valor inserido não é válido."

if __name__ == "__main__":
    # gasto = processarGastos()                             ---
    # if gasto is not None:                                    |
    #    print("\n--- Gasto Registrado com Sucesso! ---")      |
    #    print(f"Valor: R$ {gasto['valor']:.2f}")              |
    #    print(f"Tipo: {gasto['tipo']}")                        -----> Caso queira rodar localmente
    #    if gasto['descricao'] is not None:                    |
    #        print(f"Descrição: {gasto['descricao']}")         |
    #    else:                                                 |
    #        print("Descrição: (nenhuma)")                  ---
    resultado = processarGastos("55,50 Lazer Cinema com amigos") # Teste
    print(resultado) # Teste