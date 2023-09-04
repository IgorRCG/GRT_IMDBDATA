#importando as bibliotecas
from dash import Dash 
from dash_html_components import H1, Div, P, Hr
from dash_core_components import Graph, Dropdown
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = Dash(__name__)
df = pd.read_csv("dados_tratados_IMDb.csv")

#transferindo os dados do arquivo csv para serem trabalhados nos graficos
count_by_Birth_c = df['Country_Birth'].value_counts()
count_by_Birth_y = df['Birth_year'].value_counts()
count_by_Heights = df['height_meters'].value_counts()

#transferindo os dados para "top_winners" e "top_nominations" em ordem decrescente
top_winners = df.sort_values(by='Wins', ascending=False).head(10)
top_nominations = df.sort_values(by='Nominations', ascending=False).head(10)

#Parte visual da interface, onde será exposto textos, linhas e gráficos.
app.layout = Div(
    children=[
        H1(
            'DASHBOARD IMDb Top100 Celebrity',       
            style={
                'textAlign': 'center',  
                'fontFamily': 'Arial, sans-serif',                                    #definindo o estilo do texto 
                'fontSize': '38px',  
                'color': 'green',  
            }
        ),

        Hr(),  #adicionar linha

        P(  
            'Segue abaixo os gráficos com as informações das colunas do Dataset.',
            style={
                'textAlign': 'left',  
                'fontFamily': 'Arial, sans-serif',  
                'fontSize': '24px',                                                   #definindo o estilo do texto 
                'color': 'black'  
            }
        ),
        
        Dropdown(  
            id='dropdown-seletor',  
            options=[
                {'label': "Países de nascimento", "value": 'count_by_Birth_c'},
                {'label': "Ano de nascimento", "value": 'count_by_Birth_y'},
                {'label': "Altura", "value": 'count_by_Heights'},
            ],
            value='count_by_Birth_c'  # Valor inicial selecionado
        ),

        Graph( 
            id='exemplo-grafico',  
            figure={
                'data': [],
                'layout': {}
            }
        ),

        Hr(), #adicionar linha

        Graph(
            id='maiores_ganhadores',             #grafico pie de maiores ganhadores
            figure=px.pie(
                top_winners,  
                names='Name',  
                values='Wins',  
                title='Os 10 Maiores Ganhadores de prêmios do IMDb Top100 Celebrity',
                color_discrete_sequence=px.colors.qualitative.Set3  
            )
        ),

        Hr(),  #adicionar linha

        Graph(
            id='maiores_Nomeacoes',
            figure=px.pie(
                top_nominations,                #grafico pie dos mais nomeados
                names='Name',  
                values='Nominations',  
                title='Os 10 Mais nomeados em prêmios do IMDb Top100 Celebrity',  
                color_discrete_sequence=px.colors.qualitative.Set3  
            )
        ),

        Hr()  #adicionar linha
    ]
)

@app.callback(
    Output('exemplo-grafico', 'figure'),  
    Input('dropdown-seletor', 'value')  
)
def callback(selected_value):                   #aqui estarão presentes os gráficos que dependem de como o "callback" for selecionado
    if selected_value == 'count_by_Birth_c':
        data = [
            {
                'x': count_by_Birth_c.index,
                'y': count_by_Birth_c.values,
                'type': 'bar',
                'name': 'Contagem',
                'marker': {'color': 'green'}
            }
        ]
        title = 'Contagem de Pessoas por País de Nascimento'
        xaxis_title = 'Local de Nascimento'
        yaxis_title = 'Contagem'

    elif selected_value == 'count_by_Birth_y':
        data = [
            {
                'x': count_by_Birth_y.index,
                'y': count_by_Birth_y.values,
                'type': 'bar',
                'name': 'Contagem',
                'marker': {'color': 'blue'}
            }
        ]
        title = 'Contagem de Pessoas por Ano de Nascimento'
        xaxis_title = 'Ano de Nascimento'
        yaxis_title = 'Contagem'

    elif selected_value == 'count_by_Heights':
        data = [
            {
                'x': count_by_Heights.index,
                'y': count_by_Heights.values,
                'type': 'bar',
                'name': 'Contagem',
                'marker': {'color': 'purple'}
            }
        ]
        title = 'Contagem de Pessoas por Altura'
        xaxis_title = 'Altura'
        yaxis_title = 'Contagem'

    return {
        'data': data,
        'layout': {
            'title': title,
            'xaxis': {'title': xaxis_title},
            'yaxis': {'title': yaxis_title}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
