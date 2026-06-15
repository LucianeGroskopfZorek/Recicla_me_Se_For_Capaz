import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

EMAIL_REMETENTE = "reciclameseforcapaz@gmail.com"
SENHA_APP = "rhjxxsvdfkexbumy"

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SuaNovaSenha123@",
        database="recicla_me_se_for_capaz"
    )

def enviar_email(destinatario, nome, bairro, dia, tipo):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = "♻️ Lembrete de Coleta - Recicla-me Se For Capaz"

    if tipo == "Seletiva":
        instrucao = "♻️ Separe recicláveis (papel, plástico, vidro, metal) limpos e secos e deixe na calçada até as 07h."
    else:
        instrucao = "🗑️ Coloque o lixo orgânico bem ensacado na calçada antes da coleta."

    corpo = f"""Olá, {nome}!

Passando para lembrar que amanhã ({dia}) haverá coleta {tipo} no bairro {bairro}.

{instrucao}

Juntos mantemos Canoinhas limpa e sustentável! 🌱

Atenciosamente,
Equipe Recicla-me Se For Capaz
"""
    msg.attach(MIMEText(corpo, "plain"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        servidor.quit()
        print(f"E-mail enviado para {destinatario} ({bairro} - {tipo})")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")

def verificar_coletas():
    agora = datetime.now()
    amanha = agora + timedelta(days=1)

    dias_semana = {
        0: "Segunda",
        1: "Terça",
        2: "Quarta",
        3: "Quinta",
        4: "Sexta",
        5: "Sábado",
        6: "Domingo"
    }
    dia_amanha = dias_semana[amanha.weekday()]

    print(f"[{agora.strftime('%H:%M')}] Verificando coletas para amanhã: {dia_amanha}")

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    # NOVA LÓGICA: busca só quem mora no bairro com coleta amanhã
    # e respeita as preferências individuais de alerta
    cursor.execute("""
        SELECT
            u.nome        AS usuario_nome,
            u.email,
            b.nome        AS bairro,
            c.dia_semana,
            c.tipo
        FROM usuario u
        JOIN bairro b  ON u.bairro_id  = b.id
        JOIN coleta c  ON c.bairro_id  = b.id
        WHERE c.dia_semana = %s
          AND u.email IS NOT NULL
          AND u.email != ''
          AND u.bairro_id IS NOT NULL
          AND (
              (c.tipo = 'Seletiva' AND u.alerta_seletiva = 1)
              OR
              (c.tipo = 'Orgânica' AND u.alerta_comum = 1)
          )
    """, (dia_amanha,))

    coletas = cursor.fetchall()
    cursor.close()
    conexao.close()

    if not coletas:
        print("Nenhum usuário para notificar amanhã.")
        return

    print(f"{len(coletas)} e-mail(s) para enviar.")
    for coleta in coletas:
        enviar_email(
            coleta["email"],
            coleta["usuario_nome"],
            coleta["bairro"],
            coleta["dia_semana"],
            coleta["tipo"]
        )

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_coletas, "cron", hour=18, minute=0)
    scheduler.add_job(verificar_coletas, "interval", hours=1)
    scheduler.start()
    print("Sistema de alertas iniciado! Alertas serão enviados às 18h.")
    return scheduler