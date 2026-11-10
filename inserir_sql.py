import sqlite3

conexao = sqlite3.connect("/app/data/meu_banco.db", check_same_thread=False)
cursor = conexao.cursor()



cursor.execute("""
    INSERT INTO contas (titular, senha, saldo)
    VALUES
        ('Igor', 'igor', 500.0),
        ('Ana', 'ana', 500.0),
        ('Guilherme', 'guilherme', 500.0),
        ('Admin', 'admin', 1000.0)
""")
conexao.commit()

conexao.close()
print("Banco atualizado com sucesso!")