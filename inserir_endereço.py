import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO endereco (usuario_id, rua, numero, bairro, cidade, estado, cep, complemento)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

dados = (
    5,
    "Rua das Flores",
    "123",
    "Centro",
    "Canoinhas",
    "SC",
    "89460000",
    "Apto 2"
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} endereço inserido com sucesso!")

cursor.close()
conexao.close()