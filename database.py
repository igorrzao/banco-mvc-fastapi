import sqlite3

conexao = sqlite3.connect("meu_banco.db", check_same_thread=False)
cursor = conexao.cursor()

def inicializar_banco():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
                titular TEXT,
                senha TEXT,
                saldo REAL
            )
    """)
    conexao.commit()

    cursor.execute("""
    INSERT INTO contas (titular, senha, saldo)
    VALUES
        ('Admin', '123', 500.0 )
    """)
    conexao.commit()

    
    print("Banco de dados incializado com sucesso.")
