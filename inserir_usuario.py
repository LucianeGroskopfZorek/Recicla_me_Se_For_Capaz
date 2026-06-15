import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO usuario (nome, cpf, data_nascimento, email, telefone, usuario, senha_hash)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

dados = (
    "João Santos",
    "98765432100",
    "1985-03-15",
    "joao@email.com",
    "47988888888",
    "joaosantos",
    "senha456"
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} usuário inserido com sucesso!")

cursor.close()
conexao.close()