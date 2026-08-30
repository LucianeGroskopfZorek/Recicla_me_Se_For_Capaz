import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import pymysql

# ---------------------------
# CONFIGURAÇÕES
# ---------------------------

clientes = []
indice_selecionado = None

ADMIN_USUARIO = "admin"
ADMIN_SENHA = "1234"

# ---------------------------
# MYSQL
# ---------------------------

conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="reciclagem_projeto",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conexao.cursor()

# ---------------------------
# BANCO DE DADOS
# ---------------------------

def carregar_clientes():

    global clientes

    clientes.clear()

    cursor.execute("SELECT * FROM clientes")

    resultado = cursor.fetchall()

    for cliente in resultado:
        clientes.append(cliente)

# ---------------------------
# FUNÇÕES AUXILIARES
# ---------------------------

def formatar_nome(texto):
    return " ".join(p.capitalize() for p in texto.strip().split())

def corrigir_maiusculo(entry):

    texto = entry.get()

    if texto.strip() != "":

        texto_corrigido = formatar_nome(texto)

        entry.delete(0, "end")
        entry.insert(0, texto_corrigido)

def formatar_cpf_generico(entry):

    texto = "".join(filter(str.isdigit, entry.get()))[:11]

    novo = ""

    if len(texto) > 0:
        novo += texto[:3]

    if len(texto) > 3:
        novo += "." + texto[3:6]

    if len(texto) > 6:
        novo += "." + texto[6:9]

    if len(texto) > 9:
        novo += "-" + texto[9:11]

    entry.delete(0, "end")
    entry.insert(0, novo)

def formatar_data_generico(entry):

    texto = "".join(filter(str.isdigit, entry.get()))[:8]

    novo = ""

    if len(texto) > 0:
        novo += texto[:2]

    if len(texto) > 2:
        novo += "/" + texto[2:4]

    if len(texto) > 4:
        novo += "/" + texto[4:8]

    entry.delete(0, "end")
    entry.insert(0, novo)

def formatar_telefone(event=None):

    texto = "".join(filter(str.isdigit, entry_telefone.get()))[:11]

    if len(texto) <= 10:

        if len(texto) > 6:
            texto = f"({texto[:2]}) {texto[2:6]}-{texto[6:]}"

        elif len(texto) > 2:
            texto = f"({texto[:2]}) {texto[2:]}"

        elif len(texto) > 0:
            texto = f"({texto}"

    else:

        if len(texto) > 7:
            texto = f"({texto[:2]}) {texto[2:7]}-{texto[7:]}"

        elif len(texto) > 2:
            texto = f"({texto[:2]}) {texto[2:]}"

        elif len(texto) > 0:
            texto = f"({texto}"

    entry_telefone.delete(0, "end")
    entry_telefone.insert(0, texto)

def formatar_cep(event=None):

    texto = "".join(filter(str.isdigit, entry_cep.get()))[:8]

    if len(texto) > 5:
        texto = texto[:5] + "-" + texto[5:]

    entry_cep.delete(0, "end")
    entry_cep.insert(0, texto)

def calcular_idade(data_nascimento):

    try:

        nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        hoje = datetime.today()

        idade = hoje.year - nascimento.year

        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1

        return idade

    except:
        return None

def limpar_campos():

    for campo in [
        entry_nome,
        entry_cpf,
        entry_data,
        entry_email,
        entry_telefone,
        entry_rua,
        entry_numero,
        entry_bairro,
        entry_cidade,
        entry_estado,
        entry_cep,
        entry_complemento
    ]:
        campo.delete(0, "end")

def limpar_login_usuario():



    entry_login_usuario_cpf.delete(0, "end")

    entry_login_usuario_data.delete(0, "end")

# ---------------------------
# NAVEGAÇÃO
# ---------------------------

def esconder_frames():

    frame_inicial.pack_forget()
    frame_login_usuario.pack_forget()
    frame_login_admin.pack_forget()
    frame_cadastro.pack_forget()
    frame_admin.pack_forget()
    frame_usuario.pack_forget()

def mostrar_inicial():

    try:
        limpar_login_usuario()
    except:
        pass

    esconder_frames()
    frame_inicial.pack(fill="both", expand=True)

def mostrar_login_usuario():

    esconder_frames()
    frame_login_usuario.pack(fill="both", expand=True)

def mostrar_login_admin():

    esconder_frames()
    frame_login_admin.pack(fill="both", expand=True)

def mostrar_cadastro():

    if indice_selecionado is None:

        limpar_campos()

        try:
            label_msg.configure(text="")
        except:
            pass

    esconder_frames()
    frame_cadastro.pack(fill="both", expand=True)

def mostrar_admin():

    esconder_frames()
    frame_admin.pack(fill="both", expand=True)

    carregar_clientes()
    atualizar_lista()

def mostrar_painel_usuario():

    esconder_frames()
    frame_usuario.pack(fill="both", expand=True)

# ---------------------------
# CADASTRO
# ---------------------------

def cadastrar():

    nome = entry_nome.get()
    cpf = entry_cpf.get().replace(".", "").replace("-", "")
    data_nascimento = entry_data.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    rua = entry_rua.get()
    numero = entry_numero.get()
    bairro = entry_bairro.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    cep = entry_cep.get()
    complemento = entry_complemento.get()

    idade = calcular_idade(data_nascimento)

    campos = [
        nome,
        cpf,
        data_nascimento,
        email,
        telefone,
        rua,
        numero,
        bairro,
        cidade,
        estado,
        cep
    ]

    if any(c.strip() == "" for c in campos):

        label_msg.configure(
            text="Preencha todos os campos.",
            text_color="red"
        )
        return

    if len(cpf) != 11:

        label_msg.configure(
            text="CPF inválido.",
            text_color="red"
        )
        return

    if idade is None:

        label_msg.configure(
            text="Data inválida.",
            text_color="red"
        )
        return

    if idade < 18:

        label_msg.configure(
            text="Apenas maiores de 18 anos.",
            text_color="red"
        )
        return

    try:

        sql = """
        INSERT INTO clientes (
            cpf,
            nome,
            data_nascimento,
            email,
            telefone,
            rua,
            numero,
            bairro,
            cidade,
            estado,
            cep,
            complemento
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            cpf,
            nome,
            data_nascimento,
            email,
            telefone,
            rua,
            numero,
            bairro,
            cidade,
            estado,
            cep,
            complemento
        )

        cursor.execute(sql, valores)

        conexao.commit()

        carregar_clientes()
        atualizar_lista()

        label_msg.configure(
            text="Cadastro realizado com sucesso ✅",
            text_color="green"
        )

        limpar_campos()

    except pymysql.err.IntegrityError:

        label_msg.configure(
            text="CPF já cadastrado.",
            text_color="red"
        )

# ---------------------------
# LOGIN
# ---------------------------

def login_usuario():

    cpf = entry_login_usuario_cpf.get().replace(".", "").replace("-", "")
    data = entry_login_usuario_data.get()

    cursor.execute(
        "SELECT * FROM clientes WHERE cpf=%s AND data_nascimento=%s",
        (cpf, data)
    )

    cliente = cursor.fetchone()

    if cliente:

        carregar_dados_usuario(cliente)
        mostrar_painel_usuario()

    else:

        messagebox.showerror(
            "Erro",
            "CPF ou data inválidos."
        )

def login_admin():

    usuario = entry_admin_usuario.get()
    senha = entry_admin_senha.get()

    if usuario == ADMIN_USUARIO and senha == ADMIN_SENHA:

        mostrar_admin()

    else:

        messagebox.showerror(
            "Erro",
            "Login inválido."
        )

# ---------------------------
# CRUD ADMIN
# ---------------------------

def atualizar_lista():

    txt_lista.configure(state="normal")
    txt_lista.delete("1.0", "end")

    if not clientes:

        txt_lista.insert(
            "1.0",
            "Nenhum cadastro encontrado."
        )

    else:

        for i, cliente in enumerate(clientes):

            cpf = cliente["cpf"]

            cpf_formatado = (
                f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
            )

            txt_lista.insert(
                "end",
                f"{i} - {cliente['nome']} | CPF: {cpf_formatado}\n"
            )

    txt_lista.configure(state="disabled")

def selecionar_usuario(event):

    global indice_selecionado

    try:

        indice_mouse = txt_lista.index(f"@{event.x},{event.y}")

        linha = txt_lista.get(
            f"{indice_mouse} linestart",
            f"{indice_mouse} lineend"
        )

        if "-" not in linha:
            return

        indice = linha.split("-")[0].strip()

        if not indice.isdigit():
            return

        indice = int(indice)

        if indice >= len(clientes):
            return

        cliente = clientes[indice]

        indice_selecionado = indice

        entry_nome.delete(0, "end")
        entry_nome.insert(0, cliente["nome"])

        cpf = cliente["cpf"]

        cpf_formatado = (
            f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
        )

        entry_cpf.delete(0, "end")
        entry_cpf.insert(0, cpf_formatado)

        entry_data.delete(0, "end")
        entry_data.insert(0, cliente["data_nascimento"])

        entry_email.delete(0, "end")
        entry_email.insert(0, cliente["email"])

        entry_telefone.delete(0, "end")
        entry_telefone.insert(0, cliente["telefone"])

        entry_rua.delete(0, "end")
        entry_rua.insert(0, cliente["rua"])

        entry_numero.delete(0, "end")
        entry_numero.insert(0, cliente["numero"])

        entry_bairro.delete(0, "end")
        entry_bairro.insert(0, cliente["bairro"])

        entry_cidade.delete(0, "end")
        entry_cidade.insert(0, cliente["cidade"])

        entry_estado.delete(0, "end")
        entry_estado.insert(0, cliente["estado"])

        entry_cep.delete(0, "end")
        entry_cep.insert(0, cliente["cep"])

        entry_complemento.delete(0, "end")
        entry_complemento.insert(0, cliente["complemento"])

        mostrar_cadastro()

    except Exception as erro:
        print("ERRO:", erro)

def editar():

    global indice_selecionado

    if indice_selecionado is None:
        return

    cpf_original = clientes[indice_selecionado]["cpf"]

    novo_cpf = entry_cpf.get().replace(".", "").replace("-", "")

    sql = """
    UPDATE clientes
    SET
        cpf=%s,
        nome=%s,
        data_nascimento=%s,
        email=%s,
        telefone=%s,
        rua=%s,
        numero=%s,
        bairro=%s,
        cidade=%s,
        estado=%s,
        cep=%s,
        complemento=%s
    WHERE cpf=%s
    """

    valores = (
        novo_cpf,
        entry_nome.get(),
        entry_data.get(),
        entry_email.get(),
        entry_telefone.get(),
        entry_rua.get(),
        entry_numero.get(),
        entry_bairro.get(),
        entry_cidade.get(),
        entry_estado.get(),
        entry_cep.get(),
        entry_complemento.get(),
        cpf_original
    )

    try:

        cursor.execute(sql, valores)

        conexao.commit()

        carregar_clientes()
        atualizar_lista()

        limpar_campos()

        indice_selecionado = None

        label_msg.configure(
            text="Cadastro atualizado ✅",
            text_color="green"
        )

    except pymysql.err.IntegrityError:

        label_msg.configure(
            text="CPF já cadastrado.",
            text_color="red"
        )

def excluir():

    global indice_selecionado

    if indice_selecionado is None:

        messagebox.showwarning(
            "Aviso",
            "Selecione um cadastro primeiro."
        )
        return

    nome = clientes[indice_selecionado]["nome"]

    confirmar = messagebox.askyesno(
        "Confirmar Exclusão",
        f"Deseja realmente excluir o cadastro de:\n\n{nome}?"
    )

    if not confirmar:
        return

    cpf = clientes[indice_selecionado]["cpf"]

    cursor.execute(
        "DELETE FROM clientes WHERE cpf = %s",
        (cpf,)
    )

    conexao.commit()

    carregar_clientes()
    atualizar_lista()

    limpar_campos()

    indice_selecionado = None

    label_msg.configure(
        text="Cadastro removido com sucesso.",
        text_color="red"
    )

# ---------------------------
# PAINEL USUÁRIO
# ---------------------------

def carregar_dados_usuario(cliente):

    txt_usuario.configure(state="normal")
    txt_usuario.delete("1.0", "end")

    txt_usuario.insert("end", f"Nome: {cliente['nome']}\n")
    txt_usuario.insert("end", f"Rua: {cliente['rua']}\n")
    txt_usuario.insert("end", f"Bairro: {cliente['bairro']}\n\n")

    txt_usuario.insert("end", "INFORMAÇÕES DE COLETA\n")
    txt_usuario.insert("end", "-------------------------\n")
    txt_usuario.insert("end", "Dias previstos: Terça e Sexta\n")
    txt_usuario.insert("end", "Janela estimada: 08h às 14h\n")
    txt_usuario.insert("end", "Status: Programado\n")

    txt_usuario.configure(state="disabled")

# ---------------------------
# INTERFACE
# ---------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()

app.geometry("1200x850")
app.title("♻ RECICLA-ME SE FOR CAPAZ - Gestão Sustentável")

# TELA INICIAL
frame_inicial = ctk.CTkFrame(app)

ctk.CTkLabel(
    frame_inicial,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 24, "bold")
).pack(pady=20)

ctk.CTkButton(
    frame_inicial,
    text="Cadastro de Usuário",
    command=mostrar_cadastro
).pack(pady=10)

ctk.CTkButton(
    frame_inicial,
    text="Acessar Minha Área",
    command=mostrar_login_usuario
).pack(pady=10)

ctk.CTkButton(
    frame_inicial,
    text="Área Administrativa",
    command=mostrar_login_admin
).pack(pady=10)

# LOGIN USUÁRIO
frame_login_usuario = ctk.CTkFrame(app)

ctk.CTkLabel(
    frame_login_usuario,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 22, "bold")
).pack(pady=10)

ctk.CTkLabel(frame_login_usuario, text="CPF").pack()

entry_login_usuario_cpf = ctk.CTkEntry(frame_login_usuario, width=300)
entry_login_usuario_cpf.pack(pady=5)

ctk.CTkLabel(frame_login_usuario, text="Data de nascimento").pack()

entry_login_usuario_data = ctk.CTkEntry(frame_login_usuario, width=300)
entry_login_usuario_data.pack(pady=5)

ctk.CTkButton(
    frame_login_usuario,
    text="Entrar",
    command=login_usuario
).pack(pady=10)

ctk.CTkButton(
    frame_login_usuario,
    text="Voltar",
    command=mostrar_inicial
).pack(pady=5)

# LOGIN ADMIN
frame_login_admin = ctk.CTkFrame(app)

ctk.CTkLabel(
    frame_login_admin,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 22, "bold")
).pack(pady=10)

ctk.CTkLabel(frame_login_admin, text="Usuário").pack()

entry_admin_usuario = ctk.CTkEntry(frame_login_admin, width=300)
entry_admin_usuario.pack(pady=5)

ctk.CTkLabel(frame_login_admin, text="Senha").pack()

entry_admin_senha = ctk.CTkEntry(
    frame_login_admin,
    show="*",
    width=300
)
entry_admin_senha.pack(pady=5)

ctk.CTkButton(
    frame_login_admin,
    text="Entrar",
    command=login_admin
).pack(pady=10)

ctk.CTkButton(
    frame_login_admin,
    text="Voltar",
    command=mostrar_inicial
).pack(pady=5)

# CADASTRO
frame_cadastro = ctk.CTkScrollableFrame(app, width=900, height=700)

ctk.CTkLabel(
    frame_cadastro,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 22, "bold")
).pack(pady=10)

def criar_label_entry(frame, texto):

    ctk.CTkLabel(frame, text=texto).pack()

    entry = ctk.CTkEntry(frame, width=300)
    entry.pack(pady=2)

    return entry

entry_nome = criar_label_entry(frame_cadastro, "Nome")
entry_cpf = criar_label_entry(frame_cadastro, "CPF")
entry_data = criar_label_entry(frame_cadastro, "Data de nascimento")
entry_email = criar_label_entry(frame_cadastro, "E-mail")
entry_telefone = criar_label_entry(frame_cadastro, "Telefone")
entry_rua = criar_label_entry(frame_cadastro, "Rua")
entry_numero = criar_label_entry(frame_cadastro, "Número")
entry_bairro = criar_label_entry(frame_cadastro, "Bairro")
entry_cidade = criar_label_entry(frame_cadastro, "Cidade")
entry_estado = criar_label_entry(frame_cadastro, "Estado")
entry_cep = criar_label_entry(frame_cadastro, "CEP")
entry_complemento = criar_label_entry(frame_cadastro, "Complemento")

entry_cpf.bind(
    "<KeyRelease>",
    lambda e: formatar_cpf_generico(entry_cpf)
)

entry_data.bind(
    "<KeyRelease>",
    lambda e: formatar_data_generico(entry_data)
)

entry_login_usuario_cpf.bind(
    "<KeyRelease>",
    lambda e: formatar_cpf_generico(entry_login_usuario_cpf)
)

entry_login_usuario_data.bind(
    "<KeyRelease>",
    lambda e: formatar_data_generico(entry_login_usuario_data)
)

entry_telefone.bind("<KeyRelease>", formatar_telefone)
entry_cep.bind("<KeyRelease>", formatar_cep)

entry_nome.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_nome))
entry_rua.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_rua))
entry_bairro.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_bairro))
entry_cidade.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_cidade))
entry_estado.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_estado))
entry_complemento.bind("<FocusOut>", lambda e: corrigir_maiusculo(entry_complemento))

ctk.CTkButton(
    frame_cadastro,
    text="Cadastrar",
    command=cadastrar
).pack(pady=5)

ctk.CTkButton(
    frame_cadastro,
    text="Editar",
    command=editar
).pack(pady=5)

ctk.CTkButton(
    frame_cadastro,
    text="Excluir",
    command=excluir
).pack(pady=5)

ctk.CTkButton(
    frame_cadastro,
    text="Voltar",
    command=mostrar_inicial
).pack(pady=5)

label_msg = ctk.CTkLabel(frame_cadastro, text="")
label_msg.pack(pady=10)

# ADMIN
frame_admin = ctk.CTkFrame(app)

ctk.CTkLabel(
    frame_admin,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 22, "bold")
).pack(pady=10)

ctk.CTkLabel(
    frame_admin,
    text="Cadastros",
    font=("Arial", 20, "bold")
).pack(pady=10)

txt_lista = ctk.CTkTextbox(
    frame_admin,
    width=700,
    height=400
)

txt_lista.pack(pady=10)

txt_lista.bind(
    "<ButtonRelease-1>",
    selecionar_usuario
)

ctk.CTkButton(
    frame_admin,
    text="Novo Cadastro",
    command=mostrar_cadastro
).pack(pady=5)

ctk.CTkButton(
    frame_admin,
    text="Voltar",
    command=mostrar_inicial
).pack(pady=5)

# USUÁRIO
frame_usuario = ctk.CTkFrame(app)

ctk.CTkLabel(
    frame_usuario,
    text="♻ RECICLA-ME SE FOR CAPAZ",
    text_color="green",
    font=("Arial", 22, "bold")
).pack(pady=10)

ctk.CTkLabel(
    frame_usuario,
    text="Área do Usuário",
    font=("Arial", 20, "bold")
).pack(pady=10)

txt_usuario = ctk.CTkTextbox(
    frame_usuario,
    width=700,
    height=400
)

txt_usuario.pack(pady=10)

ctk.CTkButton(
    frame_usuario,
    text="Sair",
    command=mostrar_inicial
).pack(pady=10)

# INICIALIZAÇÃO

carregar_clientes()
mostrar_inicial()

app.mainloop()