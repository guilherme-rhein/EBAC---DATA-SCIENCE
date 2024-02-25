import numpy as np
import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

def prever_renda():
# Dados
    df = pd.read_csv("https://raw.githubusercontent.com/guilherme-rhein/income_prediction/main/previsao_de_renda.csv")
    df = df.drop(columns = 'Unnamed: 0')
    df.dropna(inplace=True, ignore_index=True)
    df['data_ref'] = pd.to_datetime(df['data_ref'])
    df.drop_duplicates(inplace=True, ignore_index=True)
    #Var Num
    df_numeric = (df.select_dtypes(include=['int', 'float'])
                    .drop(columns='id_cliente'))
    #Var Int, Float, Bool, dummie "sexo":
    df_numeric_bool_sexo = df[['posse_de_veiculo', 'posse_de_imovel', 
                            'qtd_filhos', 'idade','tempo_emprego', 
                            'qt_pessoas_residencia', 'renda', 'sexo']]
    #criando Dummies
    renda = df.drop(columns=['data_ref', 'id_cliente'])
    renda_dm = pd.get_dummies(data=renda)

# Modelo
    X= renda_dm.drop(columns='renda').copy()
    y= renda_dm.renda.copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=62)
    reg = DecisionTreeRegressor(max_depth=9, min_samples_leaf=6, random_state=62)
    reg.fit(X_train, y_train)
    #teste para = ava[['renda', 'pred_renda']]
    ava = renda_dm.copy()
    ava['pred_renda'] = np.round(reg.predict(X), 2)



# Entrada de Dados e Previsão
    st.write(" ")
    st.write(" ")
    st.write('----')
    st.title("Simular Previsão de Renda")
    with st.form("my_form"):
        st.subheader("Adicione seus dados nos campos abaixo:")

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
        
        submitted = st.form_submit_button("Simular")
        if submitted:
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
    
    
if __name__ == "__main__":
    prever_renda()