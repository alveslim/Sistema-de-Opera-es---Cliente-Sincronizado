import os
import json
import gspread
import pandas as pd
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# --- CONFIGURAÇÃO GOOGLE SHEETS ---
scopes = [
    ''
]

# 1. Pega a string do JSON que está escondida no .env (ou nas variáveis de ambiente do servidor)
creds_json_str = os.getenv("GOOGLE_CREDENTIALS")

# 2. Converte a string de volta para um dicionário (formato que o Python entende)
creds_dict = json.loads(creds_json_str)

# 3. Autentica usando o dicionário em vez do arquivo físico
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
client = gspread.authorize(creds)

# Abre a planilha
planilha_completa = client.open(title='avaliacoes') 
planilha = planilha_completa.get_worksheet(0)

# --- fim CONFIGURAÇÃO GOOGLE SHEETS ---

for row in planilha.get_all_values():
    #print(row)
    dado = row[0]
    #print(dado)
    