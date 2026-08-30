import pymysql

conexao = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'aula'
)

cursor = conexao.cursor()

def cadastrar():
    nome = input("Digite seu nome:")
    telefone = input("Digite seu telefone:")
    email = input("Digite seu e-mail:")
    cpf = input('Digite seu CPF:')
    endereco = input("Digite seu endereço:")

    sql = "INSERT INTO cliente (nome, telefone, email, cpf, endereco) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, telefone, email, cpf, endereco)
    cursor.execute(sql, valores)
    conexao.commit()
    print("DADOS CADASTRADOS")
#cadastrar()


def listar():
    print("LISTA DE CLIENTE \n")
    sql = "SELECT * FROM cliente"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    
    for c in resultados:
        print(f"ID:{c[0]}")
        print(f"Nome:{c[1]}")
        print(f"Telefone::{c[2]}")
        print(f"Email:{c[3]}")
        print(f"CPF:{c[4]}")
        print(f"Endereco:{c[5]}")
        print(f"-"*30)
#listar()

def excluir():
    id = input("Digite o ID do cliente:")
    sql = "DELETE FROM cliente WHERE id = %s"
    dados = (id,)
    cursor.execute(sql,dados)
    conexao.commit()
    print("Cliente excluído com sucesso!")
#excluir()

def atualizar():
    id = input ("Digite o ID do cliente:")
    novo_nome = input ("Digite o novo nome:")
    sql = "UPDATE cliente SET nome = %s WHERE id = %s"
    dados = (novo_nome, id)
    cursor.execute(sql, dados)
    conexao.commit()
    print("Nome atualizado com sucesso!")

#atualizar()

def atualizar_telefone():
    id = input("Digite o ID do cliente: ")
    novo_telefone = input("Digite o novo telefone: ")
    sql = "UPDATE cliente SET telefone = %s WHERE id = %s"
    dados = (novo_telefone, id)
    cursor.execute(sql, dados)
    conexao.commit()
    print("Telefone atualizado com sucesso!")
#atualizar_telefone()

def atualizar_email():
    id = input("Digite o ID do cliente: ")
    novo_email = input("Digite o novo e-mail: ")
    sql = "UPDATE cliente SET email = %s WHERE id = %s"
    dados = (novo_email, id)
    cursor.execute(sql, dados)
    conexao.commit()
    print("E-mail atualizado com sucesso!")
atualizar_email()
