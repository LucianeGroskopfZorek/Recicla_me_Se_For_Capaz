import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO solicitacao_cadastro (usuario_id, bairro_id, status, data)
VALUES (%s, %s, %s, NOW())
"""

dados = (
    5,
    1,
    "Pendente"
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} solicitação inserida com sucesso!")

cursor.close()
conexao.close()