import mysql.connector

def get_conexao():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SuaNovaSenha123@",
        database="recicla_me_se_for_capaz"
    )
    return conexao