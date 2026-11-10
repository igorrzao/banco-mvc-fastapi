import sqlite3

conexao = sqlite3.connect("/app/data/meu_banco.db", check_same_thread=False)
cursor = conexao.cursor()

def inicializar_banco():
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS contas (
                 titular TEXT PRIMARY KEY NOT NULL,
                 senha TEXT NOT NULL,
                 saldo REAL NOT NULL DEFAULT (0) CHECK (saldo >= 0)
                 );
    """)
    conexao.commit()

    
    print("Banco de dados inicializado com sucesso.")
