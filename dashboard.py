import pandas as pd
from dotenv import load_dotenv, find_dotenv
import plotly.express as px
import dash
from dash import dcc, html



# Carrega as variáveis de ambiente do .env (ex: OPENAI_API_KEY)
load_dotenv(find_dotenv())

CAMINHO = './datatran2022.csv'

df_sinistro = pd.read_csv(CAMINHO, encoding="Windows-1252", sep=";")


if df_sinistro['longitude'].dtype == 'object' and df_sinistro['latitude'].dtype == 'object':
  df_sinistro['longitude'] = df_sinistro['longitude'].str.replace(',', '.').astype(float)
  df_sinistro['latitude'] = df_sinistro['latitude'].str.replace(',', '.').astype(float)

grafico = px.density_map(df_sinistro, lon="longitude", lat="latitude",
                     z='mortos', map_style="open-street-map", zoom=5, radius=4)


# Quantidade de acidentes mais frequentes por tipo de pista
qntd_acidente_por_pista = df_sinistro['tipo_pista'].value_counts().reset_index()
qntd_acidente_por_pista.columns = ['Pista', 'Quantidade']
qntd_acidente_por_pista_graf = px.bar(qntd_acidente_por_pista, 
                                      x='Pista', 
                                      y='Quantidade', 
                                      title='Acidente por pista')

# Acidentes por pista e causa (top 10)
acidentes_por_pista_e_causa = df_sinistro.groupby(['tipo_pista', 'causa_acidente']).size().reset_index(name='Quantidade')
acidentes_por_pista_e_causa = acidentes_por_pista_e_causa.sort_values('Quantidade', ascending=False).head(10)
fig1 = px.bar(acidentes_por_pista_e_causa, 
              x='causa_acidente', 
              y='Quantidade', 
              color='tipo_pista',
              title='Top 10 - Acidentes por pista e causa',
              labels={'causa_acidente': 'Causa do Acidente', 'Quantidade': 'Quantidade'},
              barmode='group')


# Menores acidentes por pista e causa (bottom 10)
menores_acidentes_por_pista_e_causa = df_sinistro.groupby(['tipo_pista', 'causa_acidente']).size().reset_index(name='Quantidade')
menores_acidentes_por_pista_e_causa = menores_acidentes_por_pista_e_causa.sort_values('Quantidade', ascending=True).head(10)
fig2 = px.bar(menores_acidentes_por_pista_e_causa, 
              x='causa_acidente', 
              y='Quantidade', 
              color='tipo_pista',
              title='Bottom 10 - Acidentes por pista e causa',
              labels={'causa_acidente': 'Causa do Acidente', 'Quantidade': 'Quantidade'},
              barmode='group')


# Número de mortos por causa de acidente (top 10)
num_mortos_por_causa_de_acidente = df_sinistro.groupby('causa_acidente')['mortos'].sum().reset_index().sort_values('mortos', ascending=False).head(10)
fig3 = px.bar(num_mortos_por_causa_de_acidente, 
              x='causa_acidente', 
              y='mortos',
              title='Top 10 - Número de mortos por causa de acidente',
              labels={'causa_acidente': 'Causa do Acidente', 'mortos': 'Número de Mortos'})


# Número de feridos graves por causa de acidente (top 10)
num_feridos_graves_por_causa_de_acidente = df_sinistro.groupby('causa_acidente')['feridos_graves'].sum().reset_index().sort_values('feridos_graves', ascending=False).head(10)
fig4 = px.bar(num_feridos_graves_por_causa_de_acidente, 
              x='causa_acidente', 
              y='feridos_graves',
              title='Top 10 - Número de feridos graves por causa de acidente',
              labels={'causa_acidente': 'Causa do Acidente', 'feridos_graves': 'Número de Feridos Graves'})

# Mortes por condição climática e UF
morte_por_condicao_climatica = df_sinistro.groupby(['condicao_metereologica', 'uf'])['mortos'].sum().reset_index()
fig5 = px.bar(morte_por_condicao_climatica, 
              x='uf', 
              y='mortos', 
              color='condicao_metereologica',
              title='Número de mortos por UF e condição meteorológica',
              labels={'uf': 'UF', 'mortos': 'Número de Mortos', 'condicao_metereologica': 'Condição Meteorológica'},
              barmode='group')


# Acidentes por horário
acidente_por_horario = df_sinistro[['horario', 'data_inversa', 'tipo_acidente', 'dia_semana', 'causa_acidente']].copy()
acidente_por_horario['data'] = pd.to_datetime(acidente_por_horario['data_inversa'] + ' ' + acidente_por_horario['horario'])
acidente_por_horario['horario'] = acidente_por_horario['data'].dt.hour

acidente_por_horario_agrupado = acidente_por_horario.value_counts().groupby(['horario']).sum().reset_index(name='Quantidade')
fig6 = px.bar(acidente_por_horario_agrupado, 
              x='horario', 
              y='Quantidade',
              title='Número de acidentes por horário',
              labels={'horario': 'Horário', 'Quantidade': 'Número de Acidentes'})


# Mortos por horário e condição meteorológica
mortos_por_horario = df_sinistro[['horario', 'data_inversa', 'mortos', 'condicao_metereologica']].copy()
mortos_por_horario['data'] = pd.to_datetime(mortos_por_horario['data_inversa'] + ' ' + mortos_por_horario['horario'])
mortos_por_horario['horario'] = mortos_por_horario['data'].dt.hour

mortos_agrupados = mortos_por_horario.groupby(['condicao_metereologica', 'horario'])['mortos'].sum().reset_index()
fig7 = px.bar(mortos_agrupados, 
              x='horario', 
              y='mortos', 
              color='condicao_metereologica',
              title='Número de mortos por horário e condição meteorológica',
              labels={'horario': 'Horário', 'mortos': 'Número de Mortos', 'condicao_metereologica': 'Condição Meteorológica'},
              barmode='group')



# Cria o aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análise de Acidentes de Trânsito", style={'textAlign': 'center'}),
    
    html.Div([
        html.H2("Visão Geográfica"),
        dcc.Graph(figure=grafico)
    ], style={'padding': '20px', 'margin': '10px', 'border': '1px solid #ddd'}),
    
    html.Div([
        html.H2("Análise por Infraestrutura"),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
    ], style={'padding': '20px', 'margin': '10px', 'border': '1px solid #ddd'}),
    
    html.Div([
        html.H2("Análise de Vítimas"),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4)
    ], style={'padding': '20px', 'margin': '10px', 'border': '1px solid #ddd'}),
    
    html.Div([
        html.H2("Análise Temporal"),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6)
    ], style={'padding': '20px', 'margin': '10px', 'border': '1px solid #ddd'}),
    html.Div([
        html.H2("Mortos agrupados"),
        dcc.Graph(figure=fig7),
    ], style={'padding': '20px', 'margin': '10px', 'border': '1px solid #ddd'})
])

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)