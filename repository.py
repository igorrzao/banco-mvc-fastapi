from database import cursor, conexao
import sqlite3


def buscar_saldo(nome_usuario:str):
    cursor.execute("SELECT saldo FROM contas WHERE titular = ?", (nome_usuario,))
    resultado = cursor.fetchone()
    
    if resultado is None:
        return {"status":"erro", "motivo": "Usuário não encontrado"}
    
    return {"saldo": resultado[0]}



def verificar_credenciais(nome_usuario: str, senha_digitada: str):
    cursor.execute("SELECT saldo, senha FROM contas WHERE titular = ?", (nome_usuario,))
    resultado = cursor.fetchone()
    
    if resultado is None:
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


def buscar_usuario(nome_usuario: str):
    cursor.execute("SELECT titular FROM contas WHERE titular = ?", (nome_usuario,))
    resultado = cursor.fetchone()

    if resultado is None:
        return{"status":"erro", "mensagem":"Usuário não encontrado."}

    usuario_encontrado = resultado[0]

    return{"status":"sucesso", "mensagem":f"Usuário {usuario_encontrado} consta na tabela"}


def atualizar_saldo_transferencia(remetente:str, novo_saldo_remetente:float, destinatario:str, novo_saldo_destinatario:float):

    try:
    
        cursor.execute("""
            UPDATE contas
            SET saldo = ?
            WHERE titular = ?
        """, (novo_saldo_remetente, remetente))

        cursor.execute("""
                UPDATE contas
                SET saldo = ?
                WHERE titular = ?
            """, (novo_saldo_destinatario, destinatario))
        conexao.commit()
        return{"status":"sucesso", "mensagem":"Saldo atualizado na tabela com sucesso"}

    except sqlite3.Error as erro:
        conexao.rollback()
        print(f"Erro ao atualizar saldos da transferência: {erro}")
        return{"status":"erro", "mensagem":"Erro ao atualizar saldos da transferência"}
