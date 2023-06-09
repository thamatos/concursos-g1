##importar as bibliotecas
import os
import requests
import gspread
import pandas as pd
import numpy as np
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from pandas import DataFrame

## importar as funções de raspar concursos e automatizar textos
from funcoes_concursos import raspa_concursos, automatiza_bot1, automatiza_bot2, automatiza_bot3, automatiza_site, automatiza_reserva, automatiza_estagio
mensagem_bot1 = automatiza_bot1()
mensagem_bot2 = automatiza_bot2()
mensagem_bot3 = automatiza_bot3()

## preparando a integração com o telegram
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

## preparando a integração com o sheets
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1iJivj5y2pbfHpMR9C2CuPXIqNT9Wxa6Q06VjDxuRraA")
sheet = planilha.worksheet("usuarios")

##configurando o flask e preparando o site
app = Flask(__name__)

menu = """
<center><a href="/">Volte ao menu</a> | <a href="/concursos">Concursos Abertos</a> | <a href="/reserva">Cadastro Reserva</a> | <a href="/estagio">Vagas de Estágio</a>    </center>
"""

@app.route("/")
def index():
  titulo = 'Concursos públicos'
  texto = 'Veja as opções de editais com vagas abertas hoje:'
  return render_template('inicio.html', titulo=titulo, texto=texto)


@app.route("/concursos")
def concursos():
  texto_site = automatiza_site()
  return menu + render_template('concursos.html', dados=texto_site, titulo='Concursos Abertos')

@app.route("/reserva")
def reserva():
  texto_reserva = automatiza_reserva()
  return menu + render_template('concursos.html', dados=texto_reserva, titulo='Cadastro Reserva')

@app.route("/estagio")
def estagio():
  texto_estagio = automatiza_estagio()
  return menu + render_template('concursos.html', dados=texto_estagio, titulo='Vagas de estágio')

## telegram

## Criar a resposta do Telegram
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  lista_entrada = ["/start", "oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]
  lista_saida = ["obrigado", "obrigada", "valeu", "muito obrigado", "muito obrigada"]
  nova_mensagem = ' '
  if message.lower().strip() in lista_entrada:
    texto_mensagem = "Oi, seja muito bem-vindo(a) ao Bot do Concurso Público do site PCI Concursos! \n Escolha uma das opções abaixo: \n - Digite 1 para saber quantos concursos e quantas vagas estão abertos hoje; \n - Digite 2 para saber quantos concursos oferecem cadastro reserva; \n - Digite 3 para ver os editais de estágio abertos; \n - Digite 4 para ser adicionado ao envio de resumos semanais."
  elif message == "1":
    texto_mensagem = f'{mensagem_bot1}'
  elif message == "2":
    texto_mensagem = f'{mensagem_bot2}'
  elif message == "3":
    texto_mensagem = f'{mensagem_bot3}'
  elif message == "4":
    usuarios = sheet.findall(str(chat_id))
    if len(usuarios) >= 1:
      texto_mensagem = "Você já está cadastrado nossa lista de interessados em envios semanais :)"
    else:
      sheet.append_row([chat_id])
      texto_mensagem = "Você foi adiconado à lista de interessados em envios semanais :)"
  elif message.lower().strip() in lista_saida:
    texto_mensagem = "Que isso! Até a próxima :)"
  else:
    texto_mensagem = "Não entendi. Escreva 'oi' ou 'olá' para ver as instruções."
  nova_mensagem = {"chat_id" : chat_id, "text" : texto_mensagem}
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  print(resposta.text)
  return "ok"







