import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuaNovaSenha123@",
    database="recicla_me_se_for_capaz"
)

cursor = conexao.cursor()

sql = """
INSERT INTO coleta (bairro_id, dia_semana, horario_inicio, horario_fim)
VALUES (%s, %s, %s, %s)
"""

dados = (
    1,
    "Segunda",
    "08:00:00",
    "12:00:00"
)

cursor.execute(sql, dados)
conexao.commit()

print(f"{cursor.rowcount} coleta inserida com sucesso!")

cursor.close()
conexao.close()