from google import genai
from markdown import markdown
from xhtml2pdf import pisa
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import os

load_dotenv(find_dotenv())

CAMINHO = './datatran2022.csv'

df_sinistro = pd.read_csv(CAMINHO, encoding="Windows-1252", sep=";")

# Gera um resumo em vez de enviar tudo
resumo = {
    "dias_com_mais_acidentes": df_sinistro['dia_semana'].value_counts().head(10).to_dict(),
    "vias_mais_perigosas": df_sinistro['br'].value_counts().dropna().head(10).to_dict(),
    "cidades_com_mais_mortes": df_sinistro.groupby("municipio")['mortos'].sum().sort_values(ascending=False).head(10).to_dict(),
    "estados_com_mais_mortes": df_sinistro.groupby("uf")['mortos'].sum().sort_values(ascending=False).head(10).to_dict(),
    "principais_causas": df_sinistro['causa_acidente'].value_counts().head(10).to_dict()
}

gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt_inicial = open("./prompt.txt", "r", encoding="utf-8").read()

roteiro_de_conteudo = gemini.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=prompt_inicial.format(
        dados=resumo,
        obs='Evite usar palavras como "morte" ou "morto". Use "vítima" ou "vítimas".',
    )
).text

html = markdown(roteiro_de_conteudo)

with open("./Roteiro Criado.pdf", "w+b") as result_file:
    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html,       # page data
        dest=result_file,  # destination file
    )

    # Check for errors
    if pisa_status.err:
        print("An error occurred!")