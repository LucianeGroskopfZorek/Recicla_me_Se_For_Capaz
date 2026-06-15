import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO admin (cpf, data_nascimento, senha_hash)
VALUES (%s, %s, %s)
"""

dados = (
    "11122233344",
    "1980-01-10",
    "adminsenha123"
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} admin inserido com sucesso!")

cursor.close()
conexao.close()