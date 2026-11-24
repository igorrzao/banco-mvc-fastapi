import sqlite3

conexao = sqlite3.connect("/app/data/meu_banco.db", check_same_thread=False)
cursor = conexao.cursor()



cursor.execute("""
    INSERT INTO contas (titular, senha, saldo_centavos)
    VALUES
        ('Igor', 'igor', 50000),
        ('Ana', 'ana', 50000),
        ('Guilherme', 'guilherme', 50000),
        ('Admin', 'admin', 100000)
""")
conexao.commit()

conexao.close()
print("Banco atualizado com sucesso!")