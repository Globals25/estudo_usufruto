#!/usr/bin/env python
# coding: utf-8

# In[313]:


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback

from tqdm.auto import tqdm, trange
from pathlib import Path

# In[345]:
xlsx_path = Path(__file__).parent.parent/'data'

def carrega_carteiras_pl(periodo,taxa):
    nomes_carteiras = ["Conservadora - Análise PL",
                       "Moderada - Análise PL",
                       "Arrojada - Análise PL",
                       "Agressiva - Análise PL"]
    
    periodo_carteiras = ["10 Anos",
                         "12 Anos",
                         "14 Anos",
                         "16 Anos",
                         "18 Anos",
                         "20 Anos",
                         "22 Anos",
                         "24 Anos",
                         "26 Anos",
                         "28 Anos",
                         "30 Anos"]
    
    periodo_escolhido = periodo_carteiras[periodo]
    
    taxa_retirada = ["2.50%","3.00%","3.50%","4.00%","4.50%","5.00%","5.50%","6.00%","6.50%","7.00%"]
    taxa_escolhida = taxa_retirada[taxa]

    
    carteiras = pd.DataFrame()
    for i in range(len(nomes_carteiras)):
        caminho_arquivo_carteira = "xlsx_path/{}/{}/{}.xlsx".format(nomes_carteiras[i],
                                                                    periodo_carteiras[periodo],
                                                                    taxa_retirada[taxa])
        carteira = pd.read_excel(caminho_arquivo_carteira)
        carteira.drop(["Unnamed: 0"], axis = 1, inplace= True)
        carteira_tratada = carteira.iloc[-1].rename(nomes_carteiras[i].split()[0])
        carteiras[nomes_carteiras[i].split()[0]] = carteira_tratada
    carteiras["Taxa"] = taxa_retirada[taxa]
    carteiras["Periodo"] = periodo_carteiras[periodo]

    return carteiras


# In[362]:


def carrega_carteiras_pl_dash(periodo,taxa):
    nomes_carteiras = ["Conservadora - Análise PL",
                       "Moderada - Análise PL",
                       "Arrojada - Análise PL",
                       "Agressiva - Análise PL"]
    
    periodo_carteiras = ["10 Anos",
                         "12 Anos",
                         "14 Anos",
                         "16 Anos",
                         "18 Anos",
                         "20 Anos",
                         "22 Anos",
                         "24 Anos",
                         "26 Anos",
                         "28 Anos",
                         "30 Anos"]
    
    taxa_retirada = ["2.50%","3.00%","3.50%","4.00%","4.50%","5.00%","5.50%","6.00%","6.50%","7.00%"]

    carteiras = pd.DataFrame()
    for i in range(len(nomes_carteiras)):
        caminho_arquivo_carteira = "xlsx_path/{}/{}/{}.xlsx".format(nomes_carteiras[i],
                                                                                                             periodo,
                                                                                                             taxa)
        carteira = pd.read_excel(caminho_arquivo_carteira)
        carteira.drop(["Unnamed: 0"], axis = 1, inplace= True)
        carteira_tratada = carteira.iloc[-1].rename(nomes_carteiras[i].split()[0])
        carteiras[nomes_carteiras[i].split()[0]] = carteira_tratada
        
    return carteiras


# In[354]:


def carrega_carteiras_retornos(carteira_idx,periodo):
    nomes_carteiras = ["Conservadora - Análise PL",
                       "Moderada - Análise PL",
                       "Arrojada - Análise PL",
                       "Agressiva - Análise PL"]
    #10 Anos Conservadora - Análise PL_10 Anos
    periodo_carteiras = ["10 Anos",
                         "12 Anos",
                         "14 Anos",
                         "16 Anos",
                         "18 Anos",
                         "20 Anos",
                         "22 Anos",
                         "24 Anos",
                         "26 Anos",
                         "28 Anos",
                         "30 Anos"]
    
    periodo_escolhido = periodo_carteiras[periodo]

    carteiras = pd.DataFrame()
    #10 Anos Conservadora - Análise PL_10 Anos
    #carteiras_pl/10 Anos/Conservadora 10 - Análise PL_10 Anos.xlsx'
    caminho_arquivo_carteira = "xlsx_path/{}/{} {} - Análise PL_{}.xlsx".format(nomes_carteiras[carteira_idx],
                                                                                                                         periodo_carteiras[periodo],
                                                                                                                         nomes_carteiras[carteira_idx].split()[0],
                                                                                                                         periodo_carteiras[periodo])
    carteira = pd.read_excel(caminho_arquivo_carteira)
    carteiras = carteira.drop(["Unnamed: 0"], axis = 1)
    carteiras["Carteira"] = nomes_carteiras[carteira_idx].split()[0]
    carteiras["Periodo"] = periodo_carteiras[periodo]

    return carteiras


# In[343]:


periodo_carteiras = ["10 Anos",
                     "12 Anos",
                     "14 Anos",
                     "16 Anos",
                     "18 Anos",
                     "20 Anos",
                     "22 Anos",
                     "24 Anos",
                     "26 Anos",
                     "28 Anos",
                     "30 Anos"]

taxa_retirada = ["2.50%","3.00%","3.50%","4.00%","4.50%","5.00%","5.50%","6.00%","6.50%","7.00%"]

combinacoes = []

for i in trange(len(periodo_carteiras)):
    print(f"Período: {periodo_carteiras[i]}")
    for o in trange(len(taxa_retirada)):
        print(f"Taxa: {taxa_retirada[o]}")
        grupo_carteira = carrega_carteiras_pl(i,o)
        combinacoes.append(grupo_carteira)

dados_completos = pd.concat(combinacoes)


# In[358]:


nomes_carteiras = ["Conservadora - Análise PL",
                   "Moderada - Análise PL",
                   "Arrojada - Análise PL",
                   "Agressiva - Análise PL"]

periodo_carteiras = ["10 Anos",
                     "12 Anos",
                     "14 Anos",
                     "16 Anos",
                     "18 Anos",
                     "20 Anos",
                     "22 Anos",
                     "24 Anos",
                     "26 Anos",
                     "28 Anos",
                     "30 Anos"]
combinacoes = []

for i in trange(len(nomes_carteiras)):
    print(f"Carteira: {nomes_carteiras[i].split()[0]}")
    for o in trange(len(periodo_carteiras)):
        print(f"Periodo: {periodo_carteiras[o]}")
        grupo_carteira = carrega_carteiras_retornos(i,o)
        combinacoes.append(grupo_carteira)

dados_completos_retornos = pd.concat(combinacoes)


# ## Análise de Drawdown

# In[424]:


def calcula_drawdown(dataset):
    retornos = dataset.cummax()
    
    drawdowns = dataset/retornos - 1
    drawdown_max = drawdowns.min()
    return drawdowns*100,drawdown_max


# In[452]:


nomes_carteiras = ["Conservadora - Análise PL",
                   "Moderada - Análise PL",
                   "Arrojada - Análise PL",
                   "Agressiva - Análise PL"]

periodo_carteiras = ["10 Anos",
                     "12 Anos",
                     "14 Anos",
                     "16 Anos",
                     "18 Anos",
                     "20 Anos",
                     "22 Anos",
                     "24 Anos",
                     "26 Anos",
                     "28 Anos",
                     "30 Anos"]

maximos_dd = []

draw_downs_totais = pd.DataFrame(columns = ["Conservadora","Moderada","Arrojada","Agressiva"])
for i in range(len(nomes_carteiras)):
    dd, mdd = calcula_drawdown(dados_completos_retornos[(dados_completos_retornos["Periodo"] == "10 Anos") 
                                     & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(columns = ["Carteira","Periodo"])
                              )
    
    draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd  
        
        


# In[453]:


draw_downs_totais


# In[450]:


draw_downs_totais


# In[425]:


dd_teste, drawdown_max = calcula_drawdown(carteira_dd)


# In[471]:


def desenha_box_formatado(dataset,titulo_y,titulo_x):
    fig = px.box(dataset, color_discrete_sequence = ["black"])
    
    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend = False,height = 650, plot_bgcolor='white'
    )
    
    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,             # Exibir a grade no eixo X
        gridcolor='lightgrey',      # Cor das linhas da grade
        gridwidth=0.5,              # Largura das linhas da grade
        zeroline=True,              # Exibir linha de zero (para eixo X)
        zerolinecolor='black',      # Cor da linha de zero
        zerolinewidth=1,            # Largura da linha de zero
        showline=True,              # Exibir a linha do eixo
        linecolor='black',          # Cor da linha do eixo
        linewidth=1,                # Largura da linha do eixo,
        griddash = 'dot',
        layer="below traces"        # Coloca o Grid atrás 
    )
    
    fig.update_yaxes(
        showgrid=True,              # Exibir a grade no eixo Y
        gridcolor='lightgrey',      # Cor das linhas da grade
        gridwidth=0.5,              # Largura das linhas da grade
        zeroline=True,              # Exibir linha de zero (para eixo Y)
        zerolinecolor='black',      # Cor da linha de zero
        zerolinewidth=1,            # Largura da linha de zero
        showline=True,              # Exibir a linha do eixo
        linecolor='black',          # Cor da linha do eixo
        linewidth=1,                # Largura da linha do eixo
        griddash = 'dot',
        layer="below traces"        # Coloca o Grid atrás 
    )
    
    # Personalização das cores
    #"#392B84"
    fig.update_traces(
        marker_color="Red",       # Cor da caixa
        line_color="#272727",     # Cor da linha da borda
        fillcolor = "#6E6E6E",
        marker_size=5,            # Tamanho dos pontos
        marker_opacity=1          # Opacidade dos pontos
    )
    return fig


# ## Implementação do dashboard

# In[473]:


from dash import Dash, dcc, html, Input, Output,callback

taxa_retirada = ["2.50%","3.00%","3.50%","4.00%","4.50%","5.00%","5.50%","6.00%","6.50%","7.00%"]
periodo_carteiras = ["10 Anos",
                     "12 Anos",
                     "14 Anos",
                     "16 Anos",
                     "18 Anos",
                     "20 Anos",
                     "22 Anos",
                     "24 Anos",
                     "26 Anos",
                     "28 Anos",
                     "30 Anos"]

app = Dash(__name__)
server = app.server

app.layout = html.Div(style = {"color":"#392B84"},children=[

    # Título do Dash
    html.H1(children='Dispersão do patrimônio final para as carteiras',
           style = {'textAlign':'center'}),

    # Dropdown para a taxa
    html.Div(children='''
        Taxa
    '''),
    dcc.Dropdown(taxa_retirada,value = "2.50%", id='taxa_carteira',optionHeight=20),

    # Dropdown para o periodo

    html.Div(children='''
        Período
    ''', style = {"margin":"15px 0px 0px 0px"}),
    dcc.Dropdown(periodo_carteiras,value = "10 Anos", id='periodo_carteira',optionHeight=20),
    #margin: cima, direita, embaixo, esquerda

    # Titulo Gráfico Box - PL Final
    html.Div(children = 'Distribuição do patrimônio restante após o usufruto', id='texto_titulo', 
             style = {'textAlign':'center',
                      'font-size':'24px',
                      'margin':'20px 0px 0px 0px'}),
    
    # Subtítulo Gráfico Box - PL Final
    html.Div(id='texto_subtitulo1', style = {'textAlign':'center','font-size':'18px'}),

    # Gráfico Box - PL Final
    dcc.Graph(
        id='box_plot1',
        figure=fig
    ),

    
    # Titulo Gráfico Box - Drawdown
    html.Div(children = """Distribuição dos Drawdown's simulados para as carteiras""", 
             style = {'textAlign':'center',
                      'font-size':'24px',
                      'margin':'20px 0px 0px 0px'}),
    html.Div(id='texto_subtitulo2', style = {'textAlign':'center','font-size':'18px'}),

    dcc.Graph(
        id='box_plot2',
        figure=fig
    ),
    


])

@app.callback(
    Output('texto_subtitulo2', 'children'),
    Input('periodo_carteira','value')
)
def escreve_titulo(periodo_carteira):
    texto = f'Período: {periodo_carteira}'
    return texto

@app.callback(
    Output('texto_subtitulo1', 'children'),
    Input('periodo_carteira','value'),
    Input('taxa_carteira','value')
)
def escreve_titulo(periodo_carteira,taxa_carteira):
    texto = f'Período: {periodo_carteira} e Taxa: {taxa_carteira}'
    return texto

@app.callback(
    Output('box_plot1', 'figure'),
    Input('taxa_carteira', 'value'),
    Input('periodo_carteira','value')
)

def update_graph(taxa_carteira,periodo_carteira):

    carteiras = dados_completos[(dados_completos["Taxa"]== taxa_carteira) & (dados_completos["Periodo"]==periodo_carteira)]
    carteiras.drop(columns = ["Taxa","Periodo"], inplace = True)
    
    fig = desenha_box_formatado(carteiras,"Carteiras","Patrimônio Final [R$]")
    
    return fig

@app.callback(
    Output('box_plot2', 'figure'),
    Input('periodo_carteira','value')
)

def update_graph(periodo_carteira):

    draw_downs_totais = pd.DataFrame(columns = ["Conservadora","Moderada","Arrojada","Agressiva"])
    for i in range(len(nomes_carteiras)):
        dd, mdd = calcula_drawdown(dados_completos_retornos[(dados_completos_retornos["Periodo"] == periodo_carteira) 
                                         & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(columns = ["Carteira","Periodo"])
                                  )
        draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd  
    
    fig = desenha_box_formatado(draw_downs_totais*100, "Carteiras", "Drawdown [%]")
    
    return fig



if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




