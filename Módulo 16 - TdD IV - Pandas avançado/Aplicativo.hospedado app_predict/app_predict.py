import streamlit as st
import requests


def load_module_from_github(module_name, github_url):
    response = requests.get(github_url)
    
    if response.status_code == 200:
        module_code = response.text
        module_globals = {}
        
        try:
            exec(module_code, module_globals)
        except Exception as e:
            st.error(f"Error loading module {module_name} from {github_url}: {e}")
            return None

        if module_name in module_globals:
            return module_globals[module_name]
        else:
            st.error(f"Module {module_name} not found in loaded globals.")
            return None
    else:
        st.error(f"Failed to load module from {github_url}. Status code: {response.status_code}")
        return None

# Carrega o módulo apresentacao.py do GitHub
apresentacao = load_module_from_github("apresentacao", "https://raw.githubusercontent.com/guilherme-rhein/income_prediction/main/Aplicativo.local.final/apresentacao.py")

# Carrega o módulo prever_renda.py do GitHub
prever_renda = load_module_from_github("prever_renda", "https://raw.githubusercontent.com/guilherme-rhein/income_prediction/main/Aplicativo.local.final/previsao_renda.py")



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
        if apresentacao is not None:
            apresentacao()
    elif opcao == "Previsão de Renda":
        if prever_renda is not None:
            prever_renda()

if __name__ == "__main__":
    main()
