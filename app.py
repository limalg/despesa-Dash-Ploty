import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
#from dateutil.relativedelta import relativedelta
import pandas as pd
import pyrebase
import os
import json
from flask import session

app = dash.Dash(__name__, url_base_pathname="/dash/")

# Variáveis Globais
categorias = [
    ' ',
    'Alimentação',
    'Itens Comuns',
    'Viagem',
    'Compras Parceladas',
    'Fim de Semana',
    'Luz',
    'Condominio',
    'Gas',
    'Aluguel',
    'Investimento Foz',
    'Mercado',
    'Internet',
    'Transporte',
    'Seguro contra incêndio',
    'Pet',
    'Facily',
    'Faxina',
    'Ticket Alimentação',
    'Ticket Carro',
    'Ticket Refeição'
]

# Carregue as configurações do Firebase do arquivo JSON local
with open('firebase_config.json', 'r') as config_file:
    config = json.load(config_file)

# Configurações do Firebase
firebase_config = {
    "apiKey": config["apiKey"],
    "authDomain": config["authDomain"],
    "databaseURL": config["databaseURL"],
    "projectId": config["projectId"],
    "storageBucket": config["storageBucket"],
    "messagingSenderId": config["messagingSenderId"],
    "appId": config["appId"]
}

# Inicialize o Firebase com as configurações carregadas
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Layout do aplicativo Dash
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Página de login
login_page = html.Div([
    html.H2('Login'),
    dcc.Input(id='email', type='text', placeholder='Email'),
    dcc.Input(id='password', type='password', placeholder='Password'),
    html.Button('Login', id='login-button', n_clicks=0, style={'margin-top': '10px'})  # Botão de login
])



# Página de apresentação
presentation_page = html.Div([
    html.H2('Apresentação dos Dados'),
    # Adicione aqui os componentes para exibir os dados
])

# Página de criação
create_page = html.Div([
    html.H2('Criação de Registro'),
    # Adicione aqui os componentes para criar um novo registro
])

# Página de edição
edit_page = html.Div([
    html.H2('Edição de Registro'),
    # Adicione aqui os componentes para editar um registro
])

# Página de lista
list_page = html.Div([
    html.H2('Lista de Registros'),
    # Adicione aqui os componentes para exibir uma lista de registros
])

# Callbacks para navegação de páginas
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return login_page
    elif pathname == '/login':
        return presentation_page
    elif pathname == '/create':
        return create_page
    elif pathname == '/edit':
        return edit_page
    elif pathname == '/list':
        return list_page
    else:
        return 'Página não encontrada'

# Callbacks para autenticação
@app.callback(
    Output('url', 'pathname'),
    Input('login-button', 'n_clicks'),
    State('email', 'value'),
    State('password', 'value')
    
)
def authenticate(n_clicks, email, password):
    if n_clicks and email and password:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # Defina a sessão
            user_id = user['idToken']
            print(user)
            user_email = email
            return '/'
        except Exception as e:
            print(e)
    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
