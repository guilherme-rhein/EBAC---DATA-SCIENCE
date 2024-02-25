import streamlit as st
from apresentacao import apresentacao
from previsao_renda import prever_renda


def main():
#web
    st.set_page_config(page_title="Previsão de Renda - #Projeto",
                   page_icon="https://github.com/guilherme-rhein/income_prediction/blob/main/datasc.png?raw=true",
                   layout="wide",
                   initial_sidebar_state="auto")
#pagina
    st.markdown('<p style="font-size:100px; text-align:center"><b>Projeto</b></p>', unsafe_allow_html=True)

    st.markdown('''
    <br>
    <div style="text-align:center">
        <img src=https://github.com/guilherme-rhein/income_prediction/blob/main/google-brain-artificial-intelligence-computer-watson-brain-22e0957788960d2fb3ae9329a556f399.png?raw=true" width="400">
    </div>''', unsafe_allow_html=True)

    st.markdown('<p style="font-size:80px; text-align:center">Previsão de Renda</p>', unsafe_allow_html=True)


# Barra Lateral
    st.sidebar.markdown('''
<div style="text-align:left">
<img src="https://github.com/guilherme-rhein/income_prediction/blob/main/full.png?raw=true">
</div>
        
---                    
# **Ciência de Dados:**
## **Projeto | Previsão de renda,** [<span style="color: #8A2BE2;">GitHub</span>](https://github.com/guilherme-rhein/income_prediction.git) 

**Aluno:** *Guilherme Rhein*, [<span style="color: #8A2BE2;">LinkedIn Profile</span>](https://www.linkedin.com/in/guilherme-rhein/)<br><br>
                    
---
''', unsafe_allow_html=True)

    st.sidebar.title("Menu")
    st.sidebar.subheader("Selecione um dos campos abaixo:")
    opcao = st.sidebar.radio("Páginas", ["Sobre o Projeto", "Previsão de Renda"])

    if opcao == "Sobre o Projeto":
        apresentacao()
    elif opcao == "Previsão de Renda":
        prever_renda()

if __name__ == "__main__":
    main()