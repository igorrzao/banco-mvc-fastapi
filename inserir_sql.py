import sqlite3

conexao = sqlite3.connect("meu_banco.db")
cursor = conexao.cursor()


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
        ('Igor', 'naruto', 500.0),
        ('Naruto', 'sasuke', 500.0),
        ('Itachi', 'uchiha', 500.0)
""")
conexao.commit()

conexao.close()
print("Banco atualizado com sucesso!")