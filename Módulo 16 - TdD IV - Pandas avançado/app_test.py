import io
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree

#web
st.set_page_config(page_title="Previsão de Renda - #Projeto",
                   page_icon="https://github.com/guilherme-rhein/income_prediction/blob/main/datasc.png?raw=true",
                   layout="wide",
                   initial_sidebar_state="auto")
#barra lateral
st.sidebar.markdown('''
<div style="text-align:left">
<img src="https://github.com/guilherme-rhein/income_prediction/blob/main/full.png?raw=true">
</div>
        
---                    
# **Ciência de Dados:**
## **Projeto | Previsão de renda,** [GitHub](https://github.com/guilherme-rhein/income_prediction.git) 

**Aluno:** *Guilherme Rhein*, [**LinkedIn Profile**](https://www.linkedin.com/in/guilherme-rhein/)<br><br>
                    
---
''', unsafe_allow_html=True)


#pagina
st.markdown('<p style="font-size:100px; text-align:center"><b>Projeto</b></p>', unsafe_allow_html=True)

st.markdown('''
<br>
<div style="text-align:center">
    <img src=https://github.com/guilherme-rhein/income_prediction/blob/main/google-brain-artificial-intelligence-computer-watson-brain-22e0957788960d2fb3ae9329a556f399.png?raw=true" width="400">
</div>''', unsafe_allow_html=True)

st.markdown('<p style="font-size:80px; text-align:center">Previsão de Renda</p>', unsafe_allow_html=True)

#Importação e Tratamento dos Dados
df = pd.read_csv("https://raw.githubusercontent.com/guilherme-rhein/income_prediction/main/previsao_de_renda.csv")
df = df.drop(columns = 'Unnamed: 0')
df.dropna(inplace=True, ignore_index=True)
df['data_ref'] = pd.to_datetime(df['data_ref'])
df.drop_duplicates(inplace=True, ignore_index=True)
#Var Numericas
df_numeric = (df.select_dtypes(include=['int', 'float'])
                .drop(columns='id_cliente'))
# Correlação Geral add Int, Float, Bool + "sexo":
df_numeric_bool_sexo = df[['posse_de_veiculo', 'posse_de_imovel', 
                           'qtd_filhos', 'idade','tempo_emprego', 
                           'qt_pessoas_residencia', 'renda', 'sexo']]
#criando Dummies
renda = df.drop(columns=['data_ref', 'id_cliente'])
renda_dm = pd.get_dummies(data=renda)

#Modelo
X= renda_dm.drop(columns='renda').copy()
y= renda_dm.renda.copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=62)
reg = DecisionTreeRegressor(max_depth=9, min_samples_leaf=6, random_state=62)
reg.fit(X_train, y_train)
#teste para = ava[['renda', 'pred_renda']]
ava = renda_dm.copy()
ava['pred_renda'] = np.round(reg.predict(X), 2)


## Previsão Renda
st.write('----')
st.title("Simular Previsão de Renda")
st.markdown('### Adicione seus dados nos campos abaixo:<a name="1"></a>', unsafe_allow_html=True)


sexo = st.radio("Defina seu Gênero:", ('M', 'F'))
idade = st.slider("Defina sua Idade:", min_value=18, max_value=100, value=18)
qtd_filhos = st.slider("Defina a Quantidade de Filhos:", min_value=0, max_value=20, value=0)
tempo_emprego = st.slider("Defina o Tempo que Permanece Empregado em Anos:", min_value=0, max_value=60, value=0)
posse_de_veiculo = st.checkbox("Possuo Veículo Próprio")
posse_de_imovel = st.checkbox("Possuo Imóvel Próprio")
tipo_renda = st.selectbox("Defina seu tipo de Renda:", ['Empresário', 'Assalariado', 'Servidor público', 'Bolsista', 'Pensionista'])
educacao = st.selectbox("Defina seu Nível de Educação:", ['Secundário', 'Superior completo', 'Superior incompleto', 'Primário', 'Pós graduação'])
estado_civil = st.selectbox("Defina seu Estado Civil:", ['Solteiro', 'Casado', 'Viúvo', 'União', 'Separado'])
tipo_residencia = st.selectbox("Defina a Residência:", ['Casa', 'Governamental', 'Com os pais', 'Aluguel', 'Estúdio', 'Comunitário'])
qt_pessoas_residencia = st.number_input("Defina a Quantidade de Pessoas na Residência", min_value=1, max_value=15, value=1)
        




### Página de apresentação
@st.cache_data
def apresentacao():
    with st.sidebar.expander("Índice Geral", expanded=False):
        st.markdown('''
        - [Simulação para Previsão de Renda](#1)            
        - [Etapa 1 Crisp-DM: Entendimento do Negócio](#2)
        - [Etapa 2 Crisp-DM: Entendimento dos Dados](#3)
        - [Etapa 3 Crisp-DM: Preparação dos Dados](#4)
        - [Etapa 4 Crisp-DM: Modelagem](#5)
        - [Etapa 5 Crisp-DM: Avaliação dos Resultados](#6)
        - [Etapa 6 Crisp-DM: Implantação](#7)
    ''', unsafe_allow_html=True)
        
    st.divider()

    st.markdown('## Etapa 1 CRISP - DM: Entendimento do negócio:<a name="2"></a>', unsafe_allow_html=True)

    st.markdown('''Uma instituição financeira está empenhada em aprimorar sua compreensão acerca do perfil de renda de seus novos clientes, 
                com o intuito de otimizar a definição dos limites de cartões de crédito, sem a necessidade de solicitar comprovantes de renda 
                ou documentos que possam impactar a experiência do cliente.</p>''')
    st.markdown('''Para alcançar esse objetivo, a instituição conduziu um estudo detalhado com alguns clientes, validando suas rendas por meio de
                olerites e outros documentos. Agora, busca desenvolver um modelo preditivo para estimar a renda com base em variáveis existentes 
                em seu banco de dados, visando uma abordagem mais eficiente e personalizada.''')
    
    st.divider()
    
    st.markdown('## Etapa 2 Crisp-DM: Entendimento dos Dados:<a name="3"></a>', unsafe_allow_html=True)
    st.markdown('''#### Dicionário de dados <a name="dicionario"></a>
| Variável                | Descrição                                                                                         | Tipo         |
|-------------------------|:-------------------------------------------------------------------------------------------------:| ------------:|
| data_ref                |  Data de coleta das variáveis de referência.                                                      | Object       |
| id_cliente              |  Código identificador do cliente.                                                                 | Int          |
| sexo                    |  Gênero do cliente (M = 'Masculino'; F = 'Feminino').                                             | Object       |
| posse_de_veiculo        |  True indica posse de veículo e False indica inexistência de veículo.                             | Bool         |
| posse_de_imovel         |  True indica posse de imóvel e False indica inexistência de imóvel.                               | Bool         |
| qtd_filhos              |  Número de filhos do cliente.                                                                     | Int          |
| tipo_renda              |  Define a renda: Empresário, Assalariado, Servidor público, Pensionista, Bolsista.                | Object       |
| educacao                |  Nível de instrução: Primário, Secundário, Superior incompleto, Superior completo, Pós graduação. | Object       |
| estado_civil            |  Define o estado civil: Solteiro, União, Casado, Separado, Viúvo.                                 | Object       | 
| tipo_residencia         |  Define a residência: Casa, Governamental, Com os pais, Aluguel, Estúdio, Comunitário.            | Object       |
| idade                   |  Idade em anos.                                                                                   | Int          |
| tempo_emprego           |  Tempo que permanece estável no emprego atual.                                                    | Float        |
| qt_pessoas_residencia   |  Número de pessoas que residem no local.                                                          | Float        |
| renda                   |  Valor de renda em Reais.                                                                         | Float        |
<br>
<br>''', unsafe_allow_html=True)
    
#Tabela com dados    
    st.markdown('#### Apresentação dos Dados:')
    st.dataframe(df)
    
    st.write(" ")
    st.markdown('#### Entendimento das Variáveis:')
#Importando dados do ProfileReport no github 
    #st.components.v1.html(open("./output/renda_analysis.html", "r", encoding="utf-8").read(), width=1200, height=800, scrolling=True)
    url = "https://raw.githubusercontent.com/guilherme-rhein/income_prediction/cf94f8109c4c85c90f600bb8f6ffd3bbeb2e20e7/renda_analysis.html"
    response = requests.get(url)
    html_content = response.text
    st.components.v1.html(html_content, width=1200, height=800, scrolling=True)

#Metricas Estatística
    st.write(" ")
    st.markdown('#### Estatística em Dados Numéricos:')
    st.write(df_numeric.describe().transpose())
   

 #Graficos
    st.write(" ")
    st.markdown('#### Relação da Variável de interesse **"Renda"** com todas as outras Variáveis:')
    plt.rc('figure', figsize=(10, 25))
    fig, axes = plt.subplots(6, 2)
# Gráfico 1: sexo
    ax1 = axes[0,0]
    sns.countplot(x="sexo", data=df, dodge=True, ax = ax1)
    ax1.set_ylabel("Contagem")
    ax1.set_xlabel("Sexo")

    ax1b = ax1.twinx()
    ax1b = sns.pointplot(x="sexo", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 2: posse_de_veiculo
    ax2 = axes[0,1]
    sns.countplot(x="posse_de_veiculo", data=df, dodge=True, ax = ax2)
    ax2.set_ylabel("Contagem")
    ax2.set_xlabel("posse_de_veiculo")

    ax2b = ax2.twinx()
    ax2b = sns.pointplot(x="posse_de_veiculo", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 3: posse_de_imovel
    ax3 = axes[1,0]
    sns.countplot(x="posse_de_imovel", data=df, dodge=True, ax = ax3)
    ax3.set_ylabel("Contagem")
    ax3.set_xlabel("posse_de_imovel")

    ax3b = ax3.twinx()
    ax3b = sns.pointplot(x="posse_de_imovel", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 4: qtd_filhos
    ax4 = axes[1,1]
    sns.countplot(x="qtd_filhos", data=df, dodge=True, ax = ax4)
    ax4.set_ylabel("Contagem")
    ax4.set_xlabel("qtd_filhos")

    ax4b = ax4.twinx()
    ax4b = sns.pointplot(x="qtd_filhos", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 5: tipo_renda
    ax5 = axes[2,0]
    sns.countplot(x="tipo_renda", data=df, dodge=True, ax = ax5)
    ax5.set_ylabel("Contagem")
    ax5.set_xlabel("tipo_renda")
    ax5.set_xticklabels(ax5.get_xticklabels(), rotation=20)

    ax5b = ax5.twinx()
    ax5b = sns.pointplot(x="tipo_renda", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 6: educacao
    ax6 = axes[2,1]
    sns.countplot(x="educacao", data=df, dodge=True, ax = ax6)
    ax6.set_ylabel("Contagem")
    ax6.set_xlabel("educacao")
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=15)

    ax6b = ax6.twinx()
    ax6b = sns.pointplot(x="educacao", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 7: estado_civil
    ax7 = axes[3,0]
    sns.countplot(x="estado_civil", data=df, dodge=True, ax = ax7)
    ax7.set_ylabel("Contagem")
    ax7.set_xlabel("estado_civil")
    ax7.set_xticklabels(ax7.get_xticklabels(), rotation=15)

    ax7b = ax7.twinx()
    ax7b = sns.pointplot(x="estado_civil", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 8: tipo_residencia
    ax8 = axes[3,1]
    sns.countplot(x="tipo_residencia", data=df, dodge=True, ax = ax8)
    ax8.set_ylabel("Contagem")
    ax8.set_xlabel("tipo_residencia")
    ax8.set_xticklabels(ax8.get_xticklabels(), rotation=15)

    ax8b = ax8.twinx()
    ax8b = sns.pointplot(x="tipo_residencia", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")
    
# Gráfico 9: tempo_emprego
 #Categorizando valores:
    df_copy = df.copy()
    intervalos = [0, 8, 16, 24, 32, 40, float('inf')]
    categorias = pd.cut(df_copy['tempo_emprego'], bins=intervalos, labels=['0-8', '9-16', '17-24', '25-32', '33-40', '40+'])
    df_copy['tempo_emprego_categoria'] = categorias
 #Plot:
    ax9 = axes[4,0]
    sns.countplot(x="tempo_emprego_categoria", data=df_copy, dodge=True, ax = ax9)
    ax9.set_ylabel("Contagem")
    ax9.set_xlabel("tempo_emprego")

    ax9b = ax9.twinx()
    ax9b = sns.pointplot(x="tempo_emprego_categoria", y="renda", data=df_copy, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")

# Gráfico 10: qt_pessoas_residencia
    ax10 = axes[4,1]
    sns.countplot(x="qt_pessoas_residencia", data=df, dodge=True, ax = ax10)
    ax10.set_ylabel("Contagem")
    ax10.set_xlabel("qt_pessoas_residencia")

    ax10b = ax10.twinx()
    ax10b = sns.pointplot(x="qt_pessoas_residencia", y="renda", data=df, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")

# Gráfico 11: idade
 #Categorizando valores:
    intervalos = [0, 10, 20, 30, 40, 50, 60, float('inf')]
    categorias = pd.cut(df_copy['idade'], bins=intervalos, labels=['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '60+'])
    df_copy['idade_categoria'] = categorias
 #Plot:
    ax11 = axes[5,0]
    sns.countplot(x="idade_categoria", data=df_copy, dodge=True, ax = ax11)
    ax11.set_ylabel("Contagem")
    ax11.set_xlabel("idade")

    ax11b = ax11.twinx()
    ax11b = sns.pointplot(x="idade_categoria", y="renda", data=df_copy, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")

# Gráfico 12: data_ref
  #Categorizando valores:
    df_copy['data_categoria'] = df_copy['data_ref'].dt.to_period('M')
 #Plot:
    ax12 = axes[5,1]
    sns.countplot(x="data_categoria", data=df_copy, dodge=True, ax = ax12)
    ax12.set_ylabel("Contagem")
    ax12.set_xlabel("data_ref")
    ax12.set_xticklabels(ax12.get_xticklabels(), rotation=90)

    ax12b = ax12.twinx()
    ax12b = sns.pointplot(x="data_categoria", y="renda", data=df_copy, dodge=True, errorbar=('ci', 90), color = 'navy')
    plt.ylabel("Renda")

    plt.subplots_adjust(wspace=.5, hspace=0.5)
    st.pyplot(fig)

    
    st.markdown(''' - O resultado da variável de interesse **"renda"** relacionada com todas as outras variáveis nos gráficos acima, 
                é fundamental para desvendar padrões e insights ocultos em conjuntos de dados. Essa abordagem permite identificar correlações, 
                padrões e possíveis causas subjacentes, oferecendo uma compreensão mais profunda do contexto em que a variável de interesse está 
                inserida. Ao relacionar todas as variáveis, a análise exploratória torna-se uma ferramenta poderosa para revelar insights valiosos, 
                informando decisões e estratégias com base em uma compreensão mais completa e precisa dos dados.
 
 - Com o gráfico, conseguimos perceber o volume da informação, além do valor de renda de acordo com a categoria relacionada:
   - Em **"idade"** é possível concluir que quanto mais maduro, maior a renda e o maior volume está entre **"31-40"** anos.
 - Esclarecemos também outro fato relevante no exempo do gráfico **"posse_de_imovel":**
   - Podemos perceber que a variação de renda é muito estreira, o que acaba por linearizar os dados dificultando a possibilidade de definir padrões nas previsões.
   ''')
    
    
    st.write(" ")
    st.markdown('#### Correlação entre Variáveis:')
# Masculino = 1 e Feminino = 0
    df_numeric_bool_sexo['sexo'] = df_numeric_bool_sexo['sexo'].map({'F': 0, 'M':1})
    (df_numeric_bool_sexo.select_dtypes(include=['int', 'float','bool'])
                         .corr()
                         .iloc[6:7,:])
#Clustermap
    cmap = sns.diverging_palette(h_neg=125, 
                             h_pos=350, 
                             as_cmap=True, 
                             sep = 1,
                             center = 'light')

    clustermap = sns.clustermap(df_numeric_bool_sexo.corr(),
               figsize=(8, 8), 
               center = 0, 
               cmap=cmap)
    st.pyplot(clustermap)

#Tendencia + linha:
    st.write(" ")
    st.markdown('#### Dispersão dos Dados:')
    plt.figure(figsize=(15,11))

    sns.scatterplot(x = 'tempo_emprego'
                , y = 'renda'
                , data = df
                , alpha = .5
                , hue = 'tipo_renda'
                , size = 'idade'
               )

    sns.regplot(x = 'tempo_emprego', 
            y = 'renda', 
            data = df, 
            scatter=False, 
            color='black')
    st.pyplot(plt)
# Graf. Tendencia
    jointplt = sns.jointplot(data=df, x="tempo_emprego", y="renda", hue = 'tipo_renda')
    st.pyplot(jointplt)
    
    st.write(" ")
    st.markdown('#### Conclusões:')
    st.markdown('''  - 100% renda > 38,5% tempo_emprego > 26,5% sexo > 12,7% idade > 8,2% posse_de_veiculo 
                > 1,9% qt_pessoas_residencia > 1,5% posse_de_imovel > 0,3% qtd_filhos
 - Inicialmete podemos dizer que existe uma correlação substancialmente reduzida entre a maioria das variáveis, 
consolidando e corroborando as conclusões previamente extraídas da análise na matriz de correlação.
 
 - Ao examinar a matriz de dispersão, torna-se evidente a presença de alguns valores discrepantes na variável de renda. 
Existem alguns outliers que são de grande importância para reconhecer seu potencial impacto nos resultados da análise de tendências.''')    
    st.divider()
# Parte 3
    st.write(" ")
    st.markdown('## Etapa 3 Crisp-DM: Preparação dos dados<a name="4"></a>', unsafe_allow_html=True)
    st.markdown('#### Dados Selecionados para o Modelo:')
    st.write(" ")
    buffer = io.StringIO()
    renda.info(buf=buffer)
    st.text(buffer.getvalue())
    st.write(" ")

    st.markdown('#### Dados Selecionados Formatados em Dummies:')
    st.write(" ")
    buffer = io.StringIO()
    renda_dm.info(buf=buffer)
    st.text(buffer.getvalue())
    st.write(" ")

    st.markdown('#### Nível de Correlação entre variáveis Dummies:')
    dum_data = (renda_dm.corr()['renda']
                        .sort_values(ascending=False)
                        .to_frame()
                        .reset_index()
                        .assign(correlação_pct=lambda x: round(x.renda * 100, 2))
                        .rename(columns={'index':'Variável',
                                        'renda':'Correlação',
                                        'correlação_pct':'%'}))
    st.write(dum_data)
    
    st.divider()
# Parte 4
    st.write(" ")
    st.markdown('## Etapa 4 Crisp-DM: Modelagem <a name="5"></a>', unsafe_allow_html=True)
    st.markdown('''DecisionTreeRegressor foi a técnica definida para o modelo, é uma escolha apropriada 
                quando você está lidando com problemas em que a predição será numérica. Ele é especialmente 
                útil quando há relações não-lineares entre as variáveis independentes e a variável dependente. 
                Por outro lado, as árvores de decisão convencionais, como o DecisionTreeClassifier, são comumente 
                usadas para problemas de classificação, onde a variável de saída é categórica e representa classes 
                ou rótulos. Essas árvores são eficazes para tomar decisões com base em características discretas.''')
# Definição Profundidade e folhas
    st.markdown('#### Definindo Melhores Medidas de Profundidade e Folhagem:')
    mses = []
    ind_i = []
    ind_j = []

    for i in range(1, 15):
        for j in range(5, 20):
            regr_1 = DecisionTreeRegressor(max_depth=i, min_samples_leaf=j, random_state=62)
            regr_1.fit(X_train, y_train)
            mse1 = regr_1.score(X_test, y_test)
            mses.append(mse1)
            ind_i.append(i)
            ind_j.append(j)
        
    df_mse = pd.DataFrame({'mses': mses, 'profundidade': ind_i, 'n_minimo': ind_j})
    df_pivot = df_mse.pivot(index='profundidade', columns='n_minimo', values='mses')
    plt.figure()
    sns.heatmap(df_pivot)
    st.write(df_mse)
    st.pyplot(plt)

#Plot da Regressão
# URL da imagem no GitHub
    st.write(" ")
    st.markdown('#### Árvore de Regressão:')
    image_url = "https://github.com/guilherme-rhein/income_prediction/raw/main/Regress%C3%A3o.png"
    st.image(image_url, caption='Regressão Linear', use_column_width=True)

    st.write(" ")
    st.markdown('#### Definições da Regressão:')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('**Total de linhas e colunas de X:**', X.shape)
    with col2:
        st.write('**Base de Treino 70%:**', X_train.shape)
    with col3:
        st.write('**Base de Teste 30%:**', X_test.shape)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown(f"<p style='text-align:center;'><b>{reg}</b></p>", unsafe_allow_html=True)
    st.divider()
#Parte 5
    st.write(" ")
    st.markdown('## Etapa 5 Crisp-DM: Avaliação dos Resultados<a name="6"></a>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(" ")
        st.markdown('#### Resultados para Treino:')
        st.write('Base de 70%:', X_train.shape)
        st.write('Profundidade: 9')
        st.write('Número de Folhas: 6')
        st.write('Score do MSE: 0,4161')
        st.write(f'R²: {reg.score(X_train, y_train):.2f}')

    with col2:
        st.write(" ")
        st.markdown('#### Resultados da Predição de Renda:')
        ava[['renda', 'pred_renda']]

    with col3:
        st.write(" ")
        st.markdown('#### Resultados para Teste:')
        st.write('Base de 30%:', X_test.shape)
        st.write('Profundidade: 9')
        st.write('Número de Folhas: 6')
        st.write('Score do MSE: 0,4161')
        st.write(f'R²: {reg.score(X_test, y_test):.2f}')
# Parte 6
    st.divider()
    st.write(" ")
    st.markdown('## Etapa 6 Crisp-DM: Implantação<a name="7"></a>', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.markdown(f"<p style='text-align:left; font-size:23px;'><b>Orientações</b></p><br>", unsafe_allow_html=True)

    st.markdown(f"""<p style='text-align:left;'><b>Inicialmente, você deve ter verificado a existência de alguns campos que devem ser 
                preenchidos para que seja possível testar a implantação da "Previsão de Renda":</b></p>""", unsafe_allow_html=True)
    
    st.markdown(f"""<p style='text-align:left;'> - Caso já tenha sido preenchido, basta selecionar o botão na barra lateral 
                "Prever Renda", que o resultado irá aparecer logo abaixo dos campos de pergunta.</p>""", unsafe_allow_html=True)
    
    st.markdown(f"""<p style='text-align:left;'> - Caso ainda não tenha preenchido, clique no link abaixo para preencher 
                os dados e, logo em seguida, basta selecionar o botão na barra lateral "Prever Renda", que o resultado irá aparecer logo 
                abaixo dos campos de pergunta.</p>""", unsafe_allow_html=True)

    st.markdown('- [Preencher dados para Previsão de Renda](#1)', unsafe_allow_html=True)


### Previsão de renda
def prever_renda():
    entrada_data = {'sexo': sexo, 
                'posse_de_veiculo': posse_de_veiculo, 
                'posse_de_imovel': posse_de_imovel, 
                'qtd_filhos': qtd_filhos, 
                'tipo_renda': tipo_renda, 
                'educacao': educacao, 
                'estado_civil': estado_civil, 
                'tipo_residencia': tipo_residencia, 
                'idade': idade, 
                'tempo_emprego': tempo_emprego, 
                'qt_pessoas_residencia': qt_pessoas_residencia}

    entrada = pd.DataFrame([entrada_data])
    entrada = pd.concat([X, pd.get_dummies(entrada)]).fillna(value=0).tail(1)
    renda_prevista = reg.predict(entrada).item()
    renda_formatada = f"R${renda_prevista:.2f}".replace('.', ',')
    st.divider()
    st.markdown(f"<p style='text-align:center; font-size:45px; color: #8A2BE2;'><b>Renda Estimada: {renda_formatada}</b></p>", unsafe_allow_html=True)
    st.divider()


# Botões na barra lateral
st.sidebar.title("Menu")
st.sidebar.subheader("Selecione um dos campos abaixo:")

if st.sidebar.button("Apresentação"):
    apresentacao()

if st.sidebar.button("Prever Renda"):
    prever_renda()