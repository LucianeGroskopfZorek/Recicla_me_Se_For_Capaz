
import customtkinter as ctk

from tkinter import messagebox

from datetime import datetime

 

clientes = []

indice_selecionado = None

 

 

# ---------------------------

# Funções auxiliares

# ---------------------------

 

def validar_cpf_entry(texto):

    texto_limpo = texto.replace(".", "").replace("-", "")

    return (texto_limpo.isdigit() and len(texto_limpo) <= 11) or texto == ""

 

 

def formatar_cpf_generico(entry):

    texto = entry.get().replace(".", "").replace("-", "")

 

    if texto.isdigit() or texto == "":

        texto = texto[:11]

 

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

 

 

def formatar_cpf_cadastro(event=None):

    formatar_cpf_generico(entry_cpf)

 

 

def formatar_cpf_busca(event=None):

    formatar_cpf_generico(entry_busca)

 

 

def formatar_data(event=None):

    texto = entry_data.get().replace("/", "")

 

    if texto.isdigit() or texto == "":

        texto = texto[:8]

 

        novo = ""

        if len(texto) > 0:

            novo += texto[:2]

        if len(texto) > 2:

            novo += "/" + texto[2:4]

        if len(texto) > 4:

            novo += "/" + texto[4:8]

 

        entry_data.delete(0, "end")

        entry_data.insert(0, novo)

 

 

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

 

 

# ---------------------------

# CRUD

# ---------------------------

 

def cadastrar():

    nome = entry_nome.get()

    cpf = entry_cpf.get()

    cpf_limpo = cpf.replace(".", "").replace("-", "")

    data_nascimento = entry_data.get()

    idade = calcular_idade(data_nascimento)

    email = entry_email.get()

 

    if nome.strip() == "" or cpf.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":

        label_msg.configure(text="Erro: Todos os campos devem ser preenchidos.", text_color="red")

        return

 

    if idade is None:

        label_msg.configure(text="Erro: Data de nascimento inválida.", text_color="red")

        return

 

    if idade < 18:

        label_msg.configure(text="Erro: Cadastro permitido apenas para maiores de 18 anos.", text_color="red")

        return

 

    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:

        label_msg.configure(text="Erro: CPF inválido.", text_color="red")

        return

 

    for cliente in clientes:

        if cliente["cpf"] == cpf_limpo:

            label_msg.configure(text="Erro: CPF já cadastrado.", text_color="red")

            return

 

    if "@" not in email:

        label_msg.configure(text="Erro: E-mail inválido.", text_color="red")

        return

 

    clientes.append({

        "nome": nome,

        "cpf": cpf_limpo,

        "data_nascimento": data_nascimento,

        "email": email

    })

 

    label_msg.configure(text="Cadastro realizado com sucesso ✅", text_color="green")

    limpar_campos()

    atualizar_lista()

 

 

def editar():

    global indice_selecionado

 

    if indice_selecionado is None:

        label_msg.configure(text="Selecione um cadastro na lista.", text_color="red")

        return

 

    nome = entry_nome.get()

    cpf = entry_cpf.get()

    cpf_limpo = cpf.replace(".", "").replace("-", "")

    data_nascimento = entry_data.get()

    idade = calcular_idade(data_nascimento)

    email = entry_email.get()

 

    if nome.strip() == "" or cpf.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":

        label_msg.configure(text="Erro: Todos os campos devem ser preenchidos.", text_color="red")

        return

 

    if idade is None:

        label_msg.configure(text="Erro: Data de nascimento inválida.", text_color="red")

        return

 

    if idade < 18:

        label_msg.configure(text="Erro: Cadastro permitido apenas para maiores de 18 anos.", text_color="red")

        return

 

    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:

        label_msg.configure(text="Erro: CPF inválido.", text_color="red")

        return

 

    for i, cliente in enumerate(clientes):

        if cliente["cpf"] == cpf_limpo and i != indice_selecionado:

            label_msg.configure(text="Erro: CPF já cadastrado em outro registro.", text_color="red")

            return

 

    if "@" not in email:

        label_msg.configure(text="Erro: E-mail inválido.", text_color="red")

        return

 

    clientes[indice_selecionado] = {

        "nome": nome,

        "cpf": cpf_limpo,

        "data_nascimento": data_nascimento,

        "email": email

    }

 

    label_msg.configure(text="Cadastro atualizado com sucesso ✅", text_color="green")

    limpar_campos()

    atualizar_lista()

 

 

def excluir():

    global indice_selecionado

 

    if indice_selecionado is None:

        label_msg.configure(text="Selecione um cadastro na lista.", text_color="red")

        return

 

    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cadastro?")

 

    if confirmacao:

        clientes.pop(indice_selecionado)

        indice_selecionado = None

 

        label_msg.configure(text="Cadastro excluído com sucesso ✅", text_color="green")

        limpar_campos()

        atualizar_lista()

 

 

def atualizar_lista():

    txt_lista.configure(state="normal")

    txt_lista.delete("1.0", "end")

 

    if not clientes:

        txt_lista.insert("1.0", "Nenhum cadastro encontrado.")

    else:

        for i, cliente in enumerate(clientes):

            marcador = "→ " if i == indice_selecionado else "   "

 

            cpf = cliente["cpf"]

            cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

 

            txt_lista.insert(

                "end",

                f"{marcador}{i} - {cliente['nome']} | CPF: {cpf_formatado}\n"

            )

 

    txt_lista.configure(state="disabled")

 

 

def selecionar_usuario(event):

    global indice_selecionado

 

    linha = txt_lista.get("insert linestart", "insert lineend")

 

    if "-" in linha:

        linha_limpa = linha.replace("→", "").strip()

        indice = linha_limpa.split("-")[0].strip()

 

        if indice.isdigit():

            indice = int(indice)

 

            if indice < len(clientes):

                cliente = clientes[indice]

 

                entry_nome.delete(0, "end")

                entry_nome.insert(0, cliente["nome"])

 

                cpf = cliente["cpf"]

                cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

 

                entry_cpf.delete(0, "end")

                entry_cpf.insert(0, cpf_formatado)

 

                entry_data.delete(0, "end")

                entry_data.insert(0, cliente["data_nascimento"])

 

                entry_email.delete(0, "end")

                entry_email.insert(0, cliente["email"])

 

                indice_selecionado = indice

                atualizar_lista()

 

 

def buscar():

    cpf = entry_busca.get().replace(".", "").replace("-", "")

 

    if not cpf.isdigit() or len(cpf) != 11:

        label_msg_busca.configure(text="Informe um CPF válido com 11 números.", text_color="red")

        return

 

    for cliente in clientes:

        if cliente["cpf"] == cpf:

            label_msg_busca.configure(

                text=(

                    "Usuário encontrado ✅\n"

                    f"Nome: {cliente['nome']}\n"

                    f"CPF: {cliente['cpf']}\n"

                    f"Data de nascimento: {cliente['data_nascimento']}\n"

                    f"E-mail: {cliente['email']}"

                ),

                text_color="green"

            )

            return

 

    label_msg_busca.configure(text="Nenhum usuário encontrado.", text_color="red")

 

 

def limpar_campos():

    entry_nome.delete(0, "end")

    entry_cpf.delete(0, "end")

    entry_data.delete(0, "end")

    entry_email.delete(0, "end")

 

 

# ---------------------------

# Interface

# ---------------------------

 

app = ctk.CTk()

app.title("Recicla-me se for capaz")

app.geometry("820x520")

app.resizable(True, True)

app.configure(fg_color="#e0e0e0")

 

messagebox.showinfo(

    "Aviso Importante",

    "Os dados informados serão utilizados exclusivamente para autenticação.\n\n"

    "O CPF será utilizado apenas para identificação e login.\n\n"

    "Nenhuma informação será usada indevidamente.\n\n"

    "Sistema voltado ao acompanhamento da reciclagem."

)

 

ctk.CTkLabel(

    app,

    text="RECICLA-ME SE FOR CAPAZ",

    font=("Georgia", 24, "bold"),

    text_color="#397c5c"

).pack(pady=(20, 5))

 

tabview = ctk.CTkTabview(app, fg_color="#e0e0e0")

tabview.pack(fill="both", expand=True, padx=20, pady=10)

 

aba_cadastro = tabview.add("Cadastro")

aba_lista = tabview.add("Listar")

aba_busca = tabview.add("Buscar")

 

for aba in (aba_cadastro, aba_lista, aba_busca):

    aba.configure(fg_color="#e0e0e0")

 

 

def label(txt):

    return ctk.CTkLabel(aba_cadastro, text=txt, font=("Arial", 13, "bold"), text_color="black")

 

 

label("Nome completo").pack(anchor="w", padx=10)

entry_nome = ctk.CTkEntry(aba_cadastro)

entry_nome.pack(fill="x", padx=10, pady=5)

 

label("CPF").pack(anchor="w", padx=10)

 

vcmd = (app.register(validar_cpf_entry), "%P")

 

entry_cpf = ctk.CTkEntry(aba_cadastro, validate="key", validatecommand=vcmd)

entry_cpf.pack(fill="x", padx=10, pady=5)

entry_cpf.bind("<KeyRelease>", formatar_cpf_cadastro)

 

label("Data de nascimento").pack(anchor="w", padx=10)

entry_data = ctk.CTkEntry(aba_cadastro)

entry_data.pack(fill="x", padx=10, pady=5)

entry_data.bind("<KeyRelease>", formatar_data)

 

label("E-mail").pack(anchor="w", padx=10)

entry_email = ctk.CTkEntry(aba_cadastro)

entry_email.pack(fill="x", padx=10, pady=10)

 

frame_btn = ctk.CTkFrame(aba_cadastro, fg_color="transparent")

frame_btn.pack(fill="x", padx=10)

 

ctk.CTkButton(frame_btn, text="Cadastrar", command=cadastrar).pack(side="left", expand=True, fill="x", padx=5)

ctk.CTkButton(frame_btn, text="Editar", command=editar).pack(side="left", expand=True, fill="x", padx=5)

ctk.CTkButton(frame_btn, text="Excluir", command=excluir).pack(side="left", expand=True, fill="x", padx=5)

 

label_msg = ctk.CTkLabel(aba_cadastro, text="", font=("Arial", 13, "bold"))

label_msg.pack(pady=10)

 

txt_lista = ctk.CTkTextbox(aba_lista)

txt_lista.pack(fill="both", expand=True, padx=10, pady=10)

txt_lista.bind("<ButtonRelease>", selecionar_usuario)

 

ctk.CTkButton(aba_lista, text="Atualizar Lista", command=atualizar_lista).pack(fill="x", padx=10)

 

ctk.CTkLabel(

    aba_busca,

    text="Buscar usuário por CPF",

    font=("Arial", 13, "bold"),

    text_color="black"

).pack(pady=(20, 5))

 

vcmd_busca = (app.register(validar_cpf_entry), "%P")

 

entry_busca = ctk.CTkEntry(aba_busca, validate="key", validatecommand=vcmd_busca)

entry_busca.pack(fill="x", padx=10, pady=5)

entry_busca.bind("<KeyRelease>", formatar_cpf_busca)

 

ctk.CTkButton(aba_busca, text="Buscar", command=buscar).pack(fill="x", padx=10)

 

label_msg_busca = ctk.CTkLabel(aba_busca, text="", font=("Arial", 13, "bold"))

label_msg_busca.pack(pady=10)

 

ctk.CTkLabel(

    app,

    text="Sistema de Gestão de Reciclagem • SENAC SC • 2026",

    text_color="gray",

    font=("Arial", 11)

).pack(side="bottom", pady=10)

 

app.mainloop()