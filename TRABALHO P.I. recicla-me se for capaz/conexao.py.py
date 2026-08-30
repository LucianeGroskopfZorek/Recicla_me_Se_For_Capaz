from conexao import conectar

def cadastrar_usuario(nome, cpf, email, senha):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO USUARIO (nome, cpf, email, senha_hash)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, cpf, email, senha))
    conn.commit()

    print("Usuário cadastrado com sucesso!")
    cursor.close()
    conn.close()

cadastrar_usuario(
    nome="João Silva",
    cpf="123.456.789-00",
    email="joao@email.com",
    senha="senha123"
)