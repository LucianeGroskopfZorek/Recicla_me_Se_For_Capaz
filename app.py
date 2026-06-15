from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from alertas import iniciar_scheduler

app = Flask(__name__)
app.secret_key = "recicla_me_chave_secreta"
scheduler = iniciar_scheduler()

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SuaNovaSenha123@",
        database="recicla_me_se_for_capaz"
    )

@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    total_usuarios = 0
    total_bairros = 0
    total_coletas = 0
    if session["perfil"] == "admin":
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario")
        total_usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bairro")
        total_bairros = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM coleta")
        total_coletas = cursor.fetchone()[0]
        cursor.close()
        conexao.close()
    return render_template("index.html",
        total_usuarios=total_usuarios,
        total_bairros=total_bairros,
        total_coletas=total_coletas)

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE cpf = %s AND senha_hash = %s", (cpf, senha))
        admin = cursor.fetchone()
        if admin:
            session["usuario_id"] = admin["id"]
            session["perfil"] = "admin"
            cursor.close()
            conexao.close()
            return redirect(url_for("index"))
        cursor.execute("SELECT * FROM usuario WHERE cpf = %s AND senha_hash = %s", (cpf, senha))
        usuario = cursor.fetchone()
        if usuario:
            session["usuario_id"] = usuario["id"]
            session["perfil"] = "usuario"
            session["nome"] = usuario["nome"]
            cursor.close()
            conexao.close()
            return redirect(url_for("index"))
        erro = "CPF ou senha incorretos!"
        cursor.close()
        conexao.close()
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/usuarios")
def usuarios():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "admin":
        return redirect(url_for("index"))
    
    bairro_filtro = request.args.get("bairro_id")
    
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    if bairro_filtro:
        cursor.execute("""
            SELECT u.*, b.nome AS nome_bairro
            FROM usuario u
            LEFT JOIN bairro b ON u.bairro_id = b.id
            WHERE u.bairro_id = %s
            ORDER BY u.nome
        """, (bairro_filtro,))
    else:
        cursor.execute("""
            SELECT u.*, b.nome AS nome_bairro
            FROM usuario u
            LEFT JOIN bairro b ON u.bairro_id = b.id
            ORDER BY u.nome
        """)
    lista = cursor.fetchall()
    
    cursor.execute("SELECT id, nome FROM bairro ORDER BY nome")
    bairros = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    return render_template("usuarios.html", usuarios=lista, bairros=bairros, bairro_filtro=bairro_filtro)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "admin":
        return redirect(url_for("index"))
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        usuario = request.form["usuario"]
        senha_hash = request.form["senha_hash"]
        conexao = conectar()
        cursor = conexao.cursor()
        sql = """INSERT INTO usuario (nome, cpf, data_nascimento, email, telefone, usuario, senha_hash)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nome, cpf, data_nascimento, email, telefone, usuario, senha_hash))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for("usuarios"))
    return render_template("cadastrar.html")

@app.route("/bairros")
def bairros():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            b.id, b.nome, b.zona,
            MAX(CASE WHEN c.tipo = 'Seletiva' THEN c.dia_semana END) as seletiva,
            MAX(CASE WHEN c.tipo = 'Orgânica' THEN c.dia_semana END) as organica
        FROM bairro b
        LEFT JOIN coleta c ON c.bairro_id = b.id
        GROUP BY b.id, b.nome, b.zona
        ORDER BY b.nome
    """)
    lista_bairros = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("bairros.html", bairros=lista_bairros)

@app.route("/coletas")
def coletas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coleta")
    lista = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("coletas.html", coletas=lista)

@app.route("/meus_dados")
def meus_dados():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "usuario":
        return redirect(url_for("index"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.*, b.nome AS nome_bairro
        FROM usuario u
        LEFT JOIN bairro b ON u.bairro_id = b.id
        WHERE u.id = %s
    """, (session["usuario_id"],))
    usuario = cursor.fetchone()
    cursor.execute("SELECT id, nome FROM bairro ORDER BY nome")
    bairros = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("meus_dados.html", usuario=usuario, bairros=bairros)

@app.route("/conteudos")
def conteudos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, u.nome as autor, cat.nome as categoria
        FROM conteudo c
        JOIN usuario u ON c.id_usuario = u.id
        JOIN categoria cat ON c.id_categoria = cat.id
        ORDER BY c.criado_em DESC
    """)
    lista = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("conteudos.html", conteudos=lista)

@app.route("/conteudos/novo", methods=["GET", "POST"])
def novo_conteudo():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        titulo = request.form["titulo"]
        corpo = request.form["corpo"]
        tipo = request.form["tipo"]
        id_categoria = request.form["id_categoria"]
        cursor.execute("""
            INSERT INTO conteudo (titulo, corpo, tipo, id_usuario, id_categoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, corpo, tipo, session["usuario_id"], id_categoria))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for("conteudos"))
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("novo_conteudo.html", categorias=categorias)

@app.route("/comentarios")
def comentarios():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT cm.*, u.nome as autor, c.titulo as conteudo
        FROM comentario cm
        JOIN usuario u ON cm.id_usuario = u.id
        JOIN conteudo c ON cm.id_conteudo = c.id
        ORDER BY cm.criado_em DESC
    """)
    lista = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("comentarios.html", comentarios=lista)

@app.route("/comentarios/novo", methods=["GET", "POST"])
def novo_comentario():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        texto = request.form["texto"]
        id_conteudo = request.form["id_conteudo"]
        cursor.execute("""
            INSERT INTO comentario (texto, id_usuario, id_conteudo)
            VALUES (%s, %s, %s)
        """, (texto, session["usuario_id"], id_conteudo))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for("comentarios"))
    cursor.execute("SELECT id, titulo FROM conteudo ORDER BY titulo")
    conteudos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("novo_comentario.html", conteudos=conteudos)

@app.route("/curtir/<int:id_conteudo>", methods=["POST"])
def curtir(id_conteudo):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO curtida (id_usuario, id_conteudo)
            VALUES (%s, %s)
        """, (session["usuario_id"], id_conteudo))
        conexao.commit()
    except:
        pass
    cursor.close()
    conexao.close()
    return redirect(url_for("conteudos"))

@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "admin":
        return redirect(url_for("index"))
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        usuario = request.form["usuario"]
        cursor.execute("""
            UPDATE usuario
            SET nome=%s, cpf=%s, email=%s, telefone=%s, usuario=%s
            WHERE id=%s
        """, (nome, cpf, email, telefone, usuario, id))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for("usuarios"))
    cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/api/coletas_bairro/<int:bairro_id>")
def api_coletas_bairro(bairro_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT dia_semana, tipo 
        FROM coleta 
        WHERE bairro_id = %s
    """, (bairro_id,))
    coletas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(coletas)

@app.route("/cadastro_publico", methods=["GET", "POST"])
def cadastro_publico():
    erro = None
    sucesso = None

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM bairro ORDER BY nome")
    bairros = cursor.fetchall()
    cursor.close()
    conexao.close()

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        usuario = request.form["usuario"]
        senha_hash = request.form["senha_hash"]
        bairro_id = request.form.get("bairro_id") or None
        alerta_seletiva = 1 if request.form.get("alerta_seletiva") else 0
        alerta_comum = 1 if request.form.get("alerta_comum") else 0

        conexao = conectar()
        cursor = conexao.cursor()
        try:
            sql = """INSERT INTO usuario 
                     (nome, cpf, data_nascimento, email, telefone, usuario, senha_hash,
                      bairro_id, alerta_seletiva, alerta_comum)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nome, cpf, data_nascimento, email, telefone,
                                 usuario, senha_hash, bairro_id,
                                 alerta_seletiva, alerta_comum))
            conexao.commit()
            sucesso = "Cadastro realizado com sucesso! Agora você já pode fazer login. 🎉"
        except Exception as e:
            erro = "Erro ao cadastrar. CPF ou e-mail já podem estar em uso."
        cursor.close()
        conexao.close()

    return render_template("cadastro_publico.html",
                           erro=erro,
                           sucesso=sucesso,
                           bairros=bairros)

@app.route("/meus_dados/editar", methods=["POST"])
def editar_meus_dados():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "usuario":
        return redirect(url_for("index"))
    email = request.form["email"]
    telefone = request.form["telefone"]
    usuario = request.form["usuario"]
    nova_senha = request.form["nova_senha"]
    bairro_id = request.form.get("bairro_id") or None
    alerta_seletiva = 1 if request.form.get("alerta_seletiva") else 0
    alerta_comum = 1 if request.form.get("alerta_comum") else 0
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    try:
        if nova_senha:
            cursor.execute("""
                UPDATE usuario
                SET email=%s, telefone=%s, usuario=%s, senha_hash=%s,
                    bairro_id=%s, alerta_seletiva=%s, alerta_comum=%s
                WHERE id=%s
            """, (email, telefone, usuario, nova_senha,
                  bairro_id, alerta_seletiva, alerta_comum,
                  session["usuario_id"]))
        else:
            cursor.execute("""
                UPDATE usuario
                SET email=%s, telefone=%s, usuario=%s,
                    bairro_id=%s, alerta_seletiva=%s, alerta_comum=%s
                WHERE id=%s
            """, (email, telefone, usuario,
                  bairro_id, alerta_seletiva, alerta_comum,
                  session["usuario_id"]))
        conexao.commit()
        sucesso = "Dados atualizados com sucesso! ✅"
        cursor.execute("""
            SELECT u.*, b.nome AS nome_bairro
            FROM usuario u
            LEFT JOIN bairro b ON u.bairro_id = b.id
            WHERE u.id = %s
        """, (session["usuario_id"],))
        usuario_atualizado = cursor.fetchone()
        cursor.execute("SELECT id, nome FROM bairro ORDER BY nome")
        bairros = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template("meus_dados.html", usuario=usuario_atualizado, bairros=bairros, sucesso=sucesso)
    except Exception as e:
        cursor.close()
        conexao.close()
        conexao2 = conectar()
        cursor2 = conexao2.cursor(dictionary=True)
        cursor2.execute("""
            SELECT u.*, b.nome AS nome_bairro
            FROM usuario u
            LEFT JOIN bairro b ON u.bairro_id = b.id
            WHERE u.id = %s
        """, (session["usuario_id"],))
        usuario_atual = cursor2.fetchone()
        cursor2.execute("SELECT id, nome FROM bairro ORDER BY nome")
        bairros = cursor2.fetchall()
        cursor2.close()
        conexao2.close()
        return render_template("meus_dados.html", usuario=usuario_atual, bairros=bairros, erro=f"Erro ao atualizar: {str(e)}")

@app.route("/editar_bairro/<int:id>", methods=["GET", "POST"])
def editar_bairro(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if session["perfil"] != "admin":
        return redirect(url_for("index"))

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    erro = None
    sucesso = None

    if request.method == "POST":
        nome = request.form["nome"]
        zona = request.form["zona"]
        dia_seletiva = request.form.get("dia_seletiva") or None
        dia_comum = request.form.get("dia_comum") or None

        try:
            cursor.execute("UPDATE bairro SET nome=%s, zona=%s WHERE id=%s", (nome, zona, id))

            cursor.execute("SELECT id FROM coleta WHERE bairro_id=%s AND tipo='Seletiva'", (id,))
            col_seletiva = cursor.fetchone()
            if dia_seletiva:
                if col_seletiva:
                    cursor.execute("UPDATE coleta SET dia_semana=%s WHERE id=%s", (dia_seletiva, col_seletiva["id"]))
                else:
                    cursor.execute("INSERT INTO coleta (bairro_id, dia_semana, tipo) VALUES (%s, %s, 'Seletiva')", (id, dia_seletiva))
            else:
                if col_seletiva:
                    cursor.execute("DELETE FROM coleta WHERE id=%s", (col_seletiva["id"],))

            cursor.execute("SELECT id FROM coleta WHERE bairro_id=%s AND tipo='Orgânica'", (id,))
            col_comum = cursor.fetchone()
            if dia_comum:
                if col_comum:
                    cursor.execute("UPDATE coleta SET dia_semana=%s WHERE id=%s", (dia_comum, col_comum["id"]))
                else:
                    cursor.execute("INSERT INTO coleta (bairro_id, dia_semana, tipo) VALUES (%s, %s, 'Orgânica')", (id, dia_comum))
            else:
                if col_comum:
                    cursor.execute("DELETE FROM coleta WHERE id=%s", (col_comum["id"],))

            conexao.commit()
            sucesso = "Bairro atualizado com sucesso! ✅"
        except Exception as e:
            erro = f"Erro ao salvar: {str(e)}"

    cursor.execute("SELECT * FROM bairro WHERE id=%s", (id,))
    bairro = cursor.fetchone()
    cursor.execute("SELECT * FROM coleta WHERE bairro_id=%s AND tipo='Seletiva'", (id,))
    coleta_seletiva = cursor.fetchone()
    cursor.execute("SELECT * FROM coleta WHERE bairro_id=%s AND tipo='Orgânica'", (id,))
    coleta_comum = cursor.fetchone()
    cursor.close()
    conexao.close()

    return render_template("editar_bairro.html",
                           bairro=bairro,
                           coleta_seletiva=coleta_seletiva,
                           coleta_comum=coleta_comum,
                           erro=erro,
                           sucesso=sucesso)

if __name__ == "__main__":
    app.run(debug=True)