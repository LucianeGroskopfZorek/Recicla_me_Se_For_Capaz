import mysql.connector

# ── Conexão ──────────────────────────────────────────────
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # <-- coloque sua senha
        database="cadastro_de_aluno"
    )

# ── Cadastrar aluno ───────────────────────────────────────
def cadastrar():
    print("\n=== CADASTRAR ALUNO ===")
    nome     = input("Nome: ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")
    email    = input("E-mail: ")
    curso    = input("Curso: ")
    cidade   = input("Cidade: ")
    estado   = input("Estado (UF): ").upper()[:2]

    sql = """
        INSERT INTO aluno (nome, telefone, endereco, email, curso, cidade, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nome, telefone, endereco, email, curso, cidade, estado)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        print("✅ Aluno cadastrado com sucesso!")
    except mysql.connector.Error as e:
        print(f"❌ Erro ao cadastrar: {e}")
    finally:
        cursor.close()
        conn.close()

# ── Listar alunos ─────────────────────────────────────────
def listar():
    print("\n=== LISTA DE ALUNOS ===")
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nome, email, curso, cidade, estado FROM aluno")
        alunos = cursor.fetchall()
        if not alunos:
            print("Nenhum aluno cadastrado.")
        for a in alunos:
            print(f"[{a[0]}] {a[1]} | {a[2]} | {a[3]} | {a[4]}-{a[5]}")
    except mysql.connector.Error as e:
        print(f"❌ Erro ao listar: {e}")
    finally:
        cursor.close()
        conn.close()

# ── Menu principal ────────────────────────────────────────
def menu():
    while True:
        print("\n========== MENU ==========")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("⚠️  Opção inválida.")

# ── Iniciar ───────────────────────────────────────────────
if __name__ == "__main__":
    menu()