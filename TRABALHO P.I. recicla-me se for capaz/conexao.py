import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="recicla_me_se_for_capaz"
    )
    return conn