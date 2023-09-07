import smtplib
import sqlite3
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup
import requests
from kivy.clock import Clock
import json


url = "https://www.saojoaofarmacias.com.br/fr-pampers-confortsec-bag-super-xxg-52un/p"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

requisicao = requests.get(url, headers=headers)

soup = BeautifulSoup(requisicao.text, 'html.parser')

# lê a classe no site que contem o valor da fralda
preco_da_fralda = soup.findAll('span', class_="sjdigital-custom-apps-0-x-currencyContainer")[1]

# lê a classe no site que contem a descrição do produto
marca = soup.find('span', class_="vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview")

preco = preco_da_fralda.text.strip()

marca = marca.get_text(":")

preco1 = preco

preco1 = preco1.replace(".", "")  # remove 0 ponto

preco1 = preco1.replace(",", ".")  # troca a virgula por ponto

preco1 = preco1.replace("R$", "")  # retira o cifrão

preco1 = preco1.replace(" ", "")  # retira os espaços

preco_formatado = float(preco1)

mensagem = f'''{marca} {preco}'''

imagem = 'images/logo.png'

def consulta_dados():
    url = "https://www.saojoaofarmacias.com.br/fr-pampers-confortsec-bag-super-xxg-52un/p"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    requisicao = requests.get(url, headers=headers)

    soup = BeautifulSoup(requisicao.text, 'html.parser')

    # lê a classe no site que contem o valor da fralda
    preco_da_fralda = soup.findAll('span', class_="sjdigital-custom-apps-0-x-currencyContainer")[1]

    # lê a classe no site que contem a descrição do produto
    marca = soup.find('span',
                      class_="vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview")

    preco = preco_da_fralda.text.strip()

    marca = marca.get_text(":")

    preco1 = preco

    preco1 = preco1.replace(".", "")  # remove 0 ponto

    preco1 = preco1.replace(",", ".")  # troca a virgula por ponto

    preco1 = preco1.replace("R$", "")  # retira o cifrão

    preco1 = preco1.replace(" ", "")  # retira os espaços

    preco_formatado = float(preco1)

    mensagem = f'''{marca} {preco}'''

    imagem = 'images/logo.png'


def cria_usuario(self):
    user = self.ids.email.text
    password = self.ids.senha.text
    if not user and not password:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='É obrigatório informar os dados para cadastro!'))
        popup = Popup(title='Cadastro de Usuário', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    elif not user:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='É obrigatório cadastrar um email!'))
        popup = Popup(title='Cadastro de Usuário', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    elif not password:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='É obrigatório cadastrar uma senha!'))
        popup = Popup(title='Cadastro de Usuário', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    else:
        conn, cursor = conectar_banco_dados()
        registrar = registrar_usuario(cursor, user, password)
        fechar_conexao(conn)
        if registrar:
            contenido_popup = BoxLayout(orientation='vertical', padding=10)
            contenido_popup.add_widget(Label(text='Usuário cadastrado com sucesso!'))
            popup = Popup(title='Cadastro de Usuário', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
            popup.open()

        else:
            contenido_popup = BoxLayout(orientation='vertical', padding=10)
            contenido_popup.add_widget(Label(text='Usuário já cadastrado na base de dados!'))
            popup = Popup(title='Cadastro de Usuário', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
            popup.open()


def login(self):
    user = self.ids.email.text
    password = self.ids.senha.text
    if not user and not password:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='É obrigatório informar dados de acesso!'))
        popup = Popup(title='Login', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    elif not user:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='O email é obrigatório!'))
        popup = Popup(title='Login', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    elif not password:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='A senha é obrigatória!'))
        popup = Popup(title='Login', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()

    else:
        # conecta a banco de dados
        conn, cursor = conectar_banco_dados()
        loga = autenticar_usuario(cursor, user, password)
        # Executa e Fecha a conexão com o banco de dados
        fechar_conexao(conn)
        if loga:
            # Ação a executar após autenticar com sucesso
            self.manager.current = 'leitura'  # Abre a tela de leitura
            self.ids.email.text = ""
            self.ids.senha.text = ""

        else:
            contenido_popup = BoxLayout(orientation='vertical', padding=10)
            contenido_popup.add_widget(Label(text='Falha de Autenticação!'))
            popup = Popup(title='Login', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
            popup.open()

            self.ids.email.text = ""
            self.ids.senha.text = ""


def send_password_reset_email(self):
    user = self.ids.email.text
    password = ""
    if not user:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='Informe um email para recuperar a senha!'))
        popup = Popup(title='Recuperar Senha', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()
        #print('Informe um email para recuperar a senha!')

    else:
        conn, cursor = conectar_banco_dados()
        nova_senha(cursor, user, password)
        fechar_conexao(conn)


def criar_tabela_usuarios(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user VARCHAR (100) NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

def criar_tabela_dados(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vl_referencia INTEGER
        )
    ''')

def inserir_na_tabela_dados(cursor):
    cursor.execute('''
        INSERT INTO dados (vl_referencia) VALUES (1)
    ''')



def registrar_usuario(cursor, user, password):
    try:
        cursor.execute("INSERT INTO usuarios (user, password) VALUES (?, ?)", (user, password))
    except sqlite3.IntegrityError:
        return False
    else:
        return True


def autenticar_usuario(cursor, user, password):
    cursor.execute("SELECT * FROM usuarios WHERE user = ? AND password = ?", (user, password))
    return cursor.fetchone() is not None


def nova_senha(cursor, user, password):
    cursor.execute("SELECT password FROM usuarios WHERE user = ? AND password <> ?", (user, password))
    result = cursor.fetchone()
    if result is not None:
        # Acessando os dados retornados
        valor = result[0]
        # Enviar e-mail com link de redefinição de senha, utilizando o valor retornado
        sender_email = "marcelosds@gmail.com"
        sender_password = "ylpjujwzwsoeczjd"
        receiver_email = user
        subject = "Recuperação de senha"
        message = f"Olá,\n\nSua senha de acesso ao Coletor é: {valor}\n\n" \
                  f"Se você não solicitou a recuperação de senha, ignore este e-mail.\n\n" \
                  f"Atenciosamente,\nEquipe de suporte"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            contenido_popup = BoxLayout(orientation='vertical', padding=10)
            contenido_popup.add_widget(Label(text='E-mail enviado com sucesso.'))
            popup = Popup(title='Recuperar Senha', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
            popup.open()
            #print('Sucesso', 'E-mail enviado com sucesso.')
        except smtplib.SMTPException:
            contenido_popup = BoxLayout(orientation='vertical', padding=10)
            contenido_popup.add_widget(Label(text='Ocorreu um erro ao enviar o e-mail.'))
            popup = Popup(title='Recuperar Senha', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
            popup.open()
            #print('Erro', 'Ocorreu um erro ao enviar o e-mail.')


    else:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='Dados de cadastro não localizados!'))
        popup = Popup(title='Recuperar Senha', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()
        #print("Alerta", "Dados de cadastro não localizados!")


def conectar_banco_dados():
    # Conectando ao banco de dados (cria o arquivo se não existir)
    conn = sqlite3.connect('dados.db')

    # Criando um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Criando a tabela de usuários, se não existir
    criar_tabela_usuarios(cursor)
    criar_tabela_dados(cursor)
    cursor.execute("SELECT vl_referencia FROM dados")
    result = cursor.fetchone()
    if result is None:
        inserir_na_tabela_dados(cursor)

    return conn, cursor


def fechar_conexao(conn):
    conn.commit()
    conn.close()




def define_referencia(self):
    referencia = self.ids.valor.text
    if not referencia:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='Referência não pode ficar vazia!'))
        popup = Popup(title='Definir Referência', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()
    else:
        conn, cursor = conectar_banco_dados()
        registra_dados(cursor, referencia)
        fechar_conexao(conn)
        self.ids.valor.text = ""
        self.manager.current = 'leitura'


def registra_dados(cursor, referencia):
    try:
        cursor.execute("DELETE FROM dados WHERE vl_referencia <> 1")
        cursor.execute("UPDATE dados SET (vl_referencia) = ?", (referencia,))
    except sqlite3.IntegrityError:
        return False
    else:
        return True

def consulta_referencia(cursor):
    cursor.execute("SELECT vl_referencia FROM dados")
    resultados = cursor.fetchall()
    valor_referencia = [resultado[0] for resultado in resultados]
    return valor_referencia
    fechar_conexao(conn)

def pushbullet_noti():
    TOKEN = 'o.ityPUqlC4tHNrCbMromdgP82Xws8Kjrs'  # Passe o Token de acaesso aqui
    title = "Valor das Fraldas"
    body = f'''O Valor das Fraldas Pampers é: {preco}\n\n''' \
           f'''{url}'''
    msg = {"type": "note", "title": title, "body": body}
    # Envia requisição ao Pushbullet
    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
def mostra_mensagem():
    conn, cursor = conectar_banco_dados()
    valor_referencia = consulta_referencia(cursor)
    valor = valor_referencia
    if preco_formatado <= valor[0]:
        pushbullet_noti()
    fechar_conexao(conn)


def dispara_email():
    conn, cursor = conectar_banco_dados()
    valor_referencia = consulta_referencia(cursor)
    valor = valor_referencia
    if preco_formatado <= valor[0]:
        enviar_email()
    fechar_conexao(conn)

def enviar_email():
    vale = "Preço da fralda teve redução, vale a pena comprar."
    conn, cursor = conectar_banco_dados()
    cursor.execute("SELECT user FROM usuarios WHERE user <> 1")
    result = cursor.fetchone()
    user1 = result[0]
    # Enviar e-mail com informações dos valores
    sender_email = "marcelosds@gmail.com"
    sender_password = "ylpjujwzwsoeczjd"
    receiver_email = user1
    subject = "Valor ds Fraldas"
    message = f'''
       Prezado(a),

       Segue o valor atualizado da Fralda nas farmácias São João:
       - {marca} {preco}.

         {vale}


       Atenciosamente: Equipe de Suporte'''

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

    except smtplib.SMTPException:
        contenido_popup = BoxLayout(orientation='vertical', padding=10)
        contenido_popup.add_widget(Label(text='Ocorreu um erro ao enviar o e-mail.'))
        popup = Popup(title='Valor das Fraldas', content=contenido_popup, size_hint=(None, None), size=(1000, 200))
        popup.open()


# Clock.schedule_interval(consulta_dados, 30)
# Clock.schedule_interval(mostra_mensagem, 30)
# Clock.schedule_interval(dispara_email, 30)

consulta_dados()
mostra_mensagem()
dispara_email()









