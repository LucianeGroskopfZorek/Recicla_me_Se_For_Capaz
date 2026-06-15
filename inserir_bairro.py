import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO bairro (nome, zona, cadastrado)
VALUES (%s, %s, %s)
"""

dados = (
    "Centro",
    "Norte",
    1
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} bairro inserido com sucesso!")

cursor.close()
conexao.close()