import streamlit as st
import io

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from scipy.spatial.distance  import squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import fcluster
from gower import gower_matrix

# Definida função Dendrograma
@st.cache_data(show_spinner=False)
def dn(color_threshold: float, num_groups: int, Z: list) -> None:
    """
    Cria e exibe um dendrograma.

    Parameters:
        color_threshold (float): Valor de threshold de cor para a coloração do dendrograma.
        num_groups (int): Número de grupos para o título do dendrograma.
        Z (list): Matriz de ligação Z.

    Returns:
        None
    """
    plt.figure(figsize=(24, 6))
    plt.ylabel(ylabel='Distância')
    
    # Adicionar o número de grupos como título
    plt.title(f'Dendrograma Hierárquico - {num_groups} Grupos')

    # Criar o dendrograma com base na matriz de ligação Z
    dn = dendrogram(Z=Z, 
                    p=6, 
                    truncate_mode='level', 
                    color_threshold=color_threshold, 
                    show_leaf_counts=True, 
                    leaf_font_size=8, 
                    leaf_rotation=45, 
                    show_contracted=True)
    plt.yticks(np.linspace(0, .6, num=31))
    plt.xticks([])

    # Exibir o dendrograma criado
    st.pyplot(plt)

    # Imprimir o número de elementos em cada parte do dendrograma
    for i in dn.keys():
        st.text(f'dendrogram.{i}: {len(dn[i])}')


# Definida função com "cache_data"
@st.cache_data(show_spinner=False)
def calculo_gower(data_x, cat_features):
    return gower_matrix(data_x=data_x, cat_features=cat_features)

def main():
    # Configuração inicial da página
    st.set_page_config(
        page_title="Hierarchical Clustering",
        page_icon="https://raw.githubusercontent.com/guilherme-rhein/Agrupamento_Hierarquico/main/img/brain.png", 
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Barra lateral
    st.sidebar.markdown('''
<div style="text-align:center">
    <img src="https://raw.githubusercontent.com/guilherme-rhein/Agrupamento_Hierarquico/main/img/data_science.png" alt="Data Science" width=120%>
</div><br>
                        
### **Projeto: Agrupamento Hierárquico**
Desenvolvedor: [Guilherme Rhein](https://www.linkedin.com/in/guilherme-rhein/)    
                                             
---
''', unsafe_allow_html=True)
    

    # Expander Índice
    with st.sidebar.expander(label="Índice", expanded=False):
        st.markdown('''
- [Entendimento do Projeto](#1)
- [Análise Descritiva](#2)
- [Seleção de Variáveis de para Agrupamento](#3)
- [Agrupamentos Hierárquicos](#4)
- [Analisando os Grupos 3 e 4](#5)
- [Conclusão](#6)
''', unsafe_allow_html=True)
        

    # Expander Bibliotecas
    with st.sidebar.expander(label="Bibliotecas", expanded=False):
        st.code('''
import streamlit as st
import io

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from scipy.spatial.distance  import squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import fcluster
from gower import gower_matrix
''', language='python')
        


    st.markdown('''
<div style="text-align:center">
    <img src="https://raw.githubusercontent.com/guilherme-rhein/Agrupamento_Hierarquico/main/img/ebac_data_science.png" alt="ebac_logo-data_science" width="100%">
</div>
          
---
''', unsafe_allow_html=True)

    st.markdown('''
<a name="1"></a> 

# Agrupamento hierárquico

Neste projeto foi utilizada a base [online shoppers purchase intention](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset) de Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2018). [Web Link](https://doi.org/10.1007/s00521-018-3523-0).

A base trata de registros de 12.330 sessões de acesso a páginas, cada sessão sendo de um único usuário em um período de 12 meses, para posteriormente relacionar o design da página e o perfil do cliente.
                
*"Será que clientes com comportamento de navegação diferentes possuem propensão a compra diferente?"*

O objetivo é agrupar as sessões de acesso ao portal considerando o comportamento de acesso e informações da data, como a proximidade a uma data especial, fim de semana e o mês.
                
|Variável                |Descrição                                                                                                                      |Atributo   | 
| :--------------------- |:----------------------------------------------------------------------------------------------------------------------------  | --------: | 
|Administrative          | Quantidade de acessos em páginas administrativas                                                                              |Numérico   | 
|Administrative_Duration | Tempo de acesso em páginas administrativas                                                                                    |Numérico   | 
|Informational           | Quantidade de acessos em páginas informativas                                                                                 |Numérico   | 
|Informational_Duration  | Tempo de acesso em páginas informativas                                                                                       |Numérico   | 
|ProductRelated          | Quantidade de acessos em páginas de produtos                                                                                  |Numérico   | 
|ProductRelated_Duration | Tempo de acesso em páginas de produtos                                                                                        |Numérico   | 
|BounceRates             | *Percentual de visitantes que entram no site e saem sem acionar outros *requests* durante a sessão                            |Numérico   | 
|ExitRates               | * Soma de vezes que a página é visualizada por último em uma sessão dividido pelo total de visualizações                      |Numérico   | 
|PageValues              | * Representa o valor médio de uma página da Web que um usuário visitou antes de concluir uma transação de comércio eletrônico |Numérico   | 
|SpecialDay              | Indica a proximidade a uma data festiva (dia das mães etc)                                                                    |Numérico   | 
|Month                   | Mês                                                                                                                           |Categórico | 
|OperatingSystems        | Sistema operacional do visitante                                                                                              |Categórico | 
|Browser                 | Browser do visitante                                                                                                          |Categórico | 
|Region                  | Região                                                                                                                        |Categórico | 
|TrafficType             | Tipo de tráfego                                                                                                               |Categórico | 
|VisitorType             | Tipo de visitante: novo ou recorrente                                                                                         |Categórico | 
|Weekend                 | Indica final de semana                                                                                                        |Categórico | 
|Revenue                 | Indica se houve compra ou não                                                                                                 |Categórico |

*Variáveis calculadas pelo Google Analytics*

---''', unsafe_allow_html=True)

    st.markdown(''' 
#### Carregamento e Visualização dos Dados do Arquivo ```online_shoppers_intention.csv```
''', unsafe_allow_html=True)
    
    # Leitura do Arquivo CSV 
    df = pd.read_csv('https://raw.githubusercontent.com/guilherme-rhein/Agrupamento_Hierarquico/main/online_shoppers_intention.csv')
    st.dataframe(df)

    # Destacando Váriavel Revenue
    st.markdown(''' 
#### Destacando a Váriavel ```Revenue```
''', unsafe_allow_html=True)
    
    st.text(df.Revenue.value_counts())

    st.dataframe((pd.DataFrame({'Índice': df['Revenue'].value_counts().index,
              'Qtd.': df['Revenue'].value_counts().values,
              '%': (df['Revenue'].value_counts(normalize=True) * 100).values})
              .set_index('Índice')))
    
    st.markdown(''' 
**É válido ressaltar que o o valor de vendas feitas como ```True``` representam apenas 15,47%**.
''', unsafe_allow_html=True)

    # Criar gráfico 
    sns.countplot(x='Revenue', data=df)
    st.pyplot(plt)
    st.markdown('---')

    # Descritiva
    st.markdown(''' 
## Análise Descritiva
<a name="2"></a> 
''', unsafe_allow_html=True)
    
    # Valores missing e tamanho de df
    st.markdown(''' 
#### Estrutura dos Dados
''', unsafe_allow_html=True)
    # Imprimir informações sobre a estrutura do DataFrame
    st.info(f''' 
Quantidade de linhas = {df.shape[0]} e colunas = {df.shape[1]}\n
Quantidade de valores missing: {df.isna().sum().sum()}\n''')
    
    # Informações e detalhes do DataFrame
    st.markdown('##### Detalhamento dos dados:')
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())
    st.write(' ')
    st.markdown('#### Correlação dos dados:')
    df_select = df.select_dtypes(exclude = 'object').corr()
    df_select   
    st.markdown('#### Gráfico de Correlação:')
    sns.heatmap(df_select.corr(), cmap='inferno')
    st.pyplot(plt)
    st.markdown('---')

    # Feature selection
    st.markdown(''' 
## Seleção de Variáveis de para Agrupamento
<a name="3"></a> 
''', unsafe_allow_html=True)
    st.markdown('''
#### Variáveis que descrevam o padrão de navegação na sessão:
> **Colunas Selecionadas:**
>
> 'Administrative', 'Informational', 'ProductRelated', 'PageValues', 'OperatingSystems', 'Browser', 'TrafficType', 'VisitorType'
''')
    navigation_pattern = ['Administrative',
                      'Informational',
                      'ProductRelated',
                      'PageValues',
                      'OperatingSystems', 
                      'Browser', 
                      'TrafficType', 
                      'VisitorType']
    st.markdown(' ')
    st.markdown(' ')
    st.markdown('''
#### Variáveis que indiquem a característica da data:
> **Colunas Selecionadas:**
>
> 'SpecialDay', 'Month', 'Weekend'
''')
    date_characteristic = ['SpecialDay', 'Month', 'Weekend']


    st.markdown('## Definindo bases e tratando adequadamente')
    with st.echo():
        # Base para definida com todas as variáveis
        df_base = df[navigation_pattern + date_characteristic]
        # Formatando para Dummies
        df_base_dum = pd.get_dummies(df_base, drop_first=False)


        # Lista com nomes de colunas apenas de variáveis categóricas para listagem no modelo
        df_cat = df_base_dum.drop(columns=['ProductRelated', 'PageValues', 'SpecialDay']).columns.values
        # Listagem no modelo
        list_cat = list(True if col in df_cat else False for col in df_base_dum)

    st.markdown(' ')    
    st.markdown('#### Detalhes dos dados tratados para o modelo')  
    st.dataframe(pd.DataFrame(df_base_dum
 .dtypes
 .reset_index()
 .rename(columns={'index': 'Variável', 
                  0: 'Tipo'})
 .assign(Categorical=list_cat)))  

    st.markdown(' ')
    st.markdown(''' 
## Agrupamentos Hierárquicos
<a name="4"></a> 
''', unsafe_allow_html=True)
    st.markdown('#### Cálculo da Distância Gower')
    with st.spinner(text='Calculando distância Gower, aguarde...(Tempo previsto: 5 Minutos)'):
        with st.echo():
            # Calculando as distâncias
            gower = calculo_gower(data_x=df_base_dum, cat_features=list_cat)
#            st.dataframe(pd.DataFrame(gower).head(4))
    
    # Tabela das distancias e grupos definidos
    st.markdown('#### Conversão dos Valores da Matriz Gower em Vetores e Definição dos Grupos "n"')  
    # Converter os resultados para vetor
    gdv = squareform(X=gower, force='tovector')
    Z = linkage(y=gdv, method='complete')

    # Criar um DataFrame com n grupos
    z_gdv = pd.DataFrame(data=Z, columns=['id1', 'id2', 'dist', 'n'])
    st.dataframe(z_gdv)

    # Criar dendrogramas:
    st.markdown('#### Dendrogramas com Número de Grupos Definidos')
    dn(color_threshold=.53, num_groups=3, Z=Z)
    dn(color_threshold=.5, num_groups=4, Z=Z)


    # Análise dos grupos 
    st.markdown('''
## Analisando os ```Grupos 3 e 4```
<a name="5"></a> 
''', unsafe_allow_html=True)
    
    st.markdown('''
##### A Variável Definida como ```3_grupos Representa a Seleção de 3 Grupos```, assim como ```4_grupos Representa a Seleção de 4 Grupos```
''', unsafe_allow_html=True)
    # Criamos uma coluna '3_grupos' 
    df['3_grupos'] = fcluster(Z=Z, t=3, criterion='maxclust')
    df['4_grupos'] = fcluster(Z=Z, t=4, criterion='maxclust')

    with st.echo():
        # Observações por nº de grupo n
        g3 = (pd.DataFrame({'Nº Grupo': df['3_grupos'].value_counts().index,
                    'Observações g3': df['3_grupos'].value_counts().values})
                    .set_index('Nº Grupo'))

        g4 = (pd.DataFrame({'Nº Grupo': df['4_grupos'].value_counts().index,
                    'Observações g4': df['4_grupos'].value_counts().values})
                    .set_index('Nº Grupo'))
        st.dataframe(g3)
        st.dataframe(g4)

    st.markdown('''
> Percebemos que nas ```observações g3``` a coluna ```N° Grupo = 1 com 9.222 Observações``` é quebrada 
em outros dois grupos quando verificado nas ```observações g4``` na coluna com ```N° Grupo = 2 com 6.666 Observações e N° Grupo 1 com 2556 Observações.```
''', unsafe_allow_html=True)


    # Realizando Tabela cruzada
    st.markdown('''
#### Tabelas Cruzadas Utilizando Váriaveis e Grupos Definidos
''', unsafe_allow_html=True)  
    st.markdown('''
##### Grupo 3 - 'VisitorType', 'Revenue'
''', unsafe_allow_html=True) 
    
    with st.echo():    
        #"3_grupos"
        # Cross-Table entre 'VisitorType', 'Revenue'
        st.dataframe((pd.crosstab(index=df.VisitorType, 
                    columns=[df['3_grupos'], df['Revenue']], 
                    normalize='all')
        .map(lambda x: f'{x*100:.0f} %')))

    st.markdown('''
##### Grupo 4 - 'VisitorType', 'Revenue'
''', unsafe_allow_html=True) 
    
    with st.echo():    
        #"4_grupos"
        # Cross-Table entre 'VisitorType', 'Revenue'
        st.dataframe((pd.crosstab(index=df.VisitorType, 
                    columns=[df['4_grupos'], df['Revenue']], 
                    normalize='all')
        .map(lambda x: f'{x*100:.0f} %')))

    st.markdown('''
##### Grupo 3 - 'Revenue'
''', unsafe_allow_html=True) 
    with st.echo():  
        #"3_grupos"
        # Cross-Table com 'Revenue'  
        st.dataframe((pd.crosstab(index=df['Revenue'], 
                    columns=df['3_grupos'], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')
        ))
    st.markdown('''
##### Grupo 4 - 'Revenue'
''', unsafe_allow_html=True) 
    with st.echo():
        #"4_grupos"
        # Cross-Table com 'Revenue'  
        st.dataframe((pd.crosstab(index=df['Revenue'], 
                    columns=df['4_grupos'], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')
        ))

    st.markdown('''
##### Grupo 3 - 'Month', 'Revenue'
''', unsafe_allow_html=True) 
    with st.echo():
        #"3_grupos"
        # Cross-Table entre 'Month', 'Revenue'
        st.dataframe((pd.crosstab(index=df['Month'], 
                    columns=[df['3_grupos'], df['Revenue']], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')
        ))
    st.markdown('''
##### Grupo 4 - 'Month', 'Revenue'
''', unsafe_allow_html=True) 
    with st.echo():
        #"4_grupos"
        # Cross-Table entre 'Month', 'Revenue'
         st.dataframe((pd.crosstab(index=df['Month'], 
                    columns=[df['4_grupos'], df['Revenue']], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')
        ))


    st.markdown('''
##### Grupo 3 - 'Revenue', 'VisitorType', 'SpecialDay'
''', unsafe_allow_html=True) 
    with st.echo():
        #"3_grupos"
        # Cross-Table entre 'Revenue', 'VisitorType', 'SpecialDay'  
        st.dataframe((pd.crosstab(index=[df.Revenue, df.VisitorType, df.SpecialDay], 
                    columns=df['3_grupos'], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')))
    st.markdown('''
##### Grupo 4 - 'Revenue', 'VisitorType', 'SpecialDay'
''', unsafe_allow_html=True) 
    with st.echo():
        #"4_grupos"
        # Cross-Table entre 'Revenue', 'VisitorType', 'SpecialDay'  
        st.dataframe((pd.crosstab(index=[df.Revenue, df.VisitorType, df.SpecialDay], 
                    columns=df['4_grupos'], 
                    normalize='all')
        .map(lambda x: f'{x*100:.2f} %')))


    # Análise dos grupos 
    st.markdown('''
## Conclusão Final
<a name="6"></a> 
''', unsafe_allow_html=True)
    
    st.markdown('''
> Observando a coluna ```3_grupos``` conseguimos concluir que ```Returning_Visitor``` sendo este do ```Grupo 1``` 
possuem maior chance de realizar uma compra. O mesmo ocorre com ```New_Visitor``` sendo do ```Grupo 2``` também 
possuem maior chance de realizar a compra.
> 
> Essa conclusão pode ser sustentada através das tabelas entre as variáveis de navegação e as características 
temporais que utilizamos como o mês ou data especial, que resultaram em insight poderosos podendo levar a equipe 
responsável a otimizar a experiência do usuário alcançando novos objetivos partindo de novas estratégias baseada 
em informação.
''', unsafe_allow_html=True)    

    


if __name__ == '__main__':
    main()