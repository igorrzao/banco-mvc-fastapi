from database import cursor, conexao


def buscar_saldo(nome_usuario:str):
    cursor.execute("SELECT saldo FROM contas WHERE titular = ?", (nome_usuario,))
    resultado = cursor.fetchone()
    
    if resultado == None:
        return {"status":"erro", "motivo": "Usuário não encontrado"}
    
    return {"status": "sucesso", "titular": nome_usuario, "saldo": resultado[0]}



def verificar_credenciais(nome_usuario: str, senha_digitada: str):
    cursor.execute("SELECT saldo, senha FROM contas WHERE titular = ?", (nome_usuario,))
    resultado = cursor.fetchone()
    
    if resultado == None:
        return{"status":"erro", "motivo":"Usuário não encontrado."}
    
    saldo_banco = resultado[0]
    senha_banco = resultado[1]

    if senha_digitada == senha_banco:
        return{"status":"sucesso", "saldo":saldo_banco}
    else:
        return{"status":"erro", "motivo":"Senha incorreta."}


def atualizar_saldo(nome_usuario:str, novo_saldo:float):
    
    cursor.execute("""
        UPDATE contas
        SET saldo = ?
        WHERE titular = ?
    """, (novo_saldo, nome_usuario))

    conexao.commit()
    return True
