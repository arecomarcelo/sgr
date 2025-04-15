# app.py
import os
import django
import streamlit as st

# Configuração da página (DEVE SER A PRIMEIRA COISA NO SCRIPT)
st.set_page_config(
    page_title="SGR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Importações após a configuração da página
from service import UserService, DataService as AppDataService
from modules import menu
from login import login_screen
from estoque import main as estoque_main
from extratos import main as extratos_main
from boletos import main as boletos_main
from vendas import main  as vendas_main

# Instanciar DataService e UserService
data_service = AppDataService()  # Renomeado para evitar conflito com o DataService de vendas
user_service = UserService(data_service)

def main():
    """
    Função principal do aplicativo
    """
    # Verificar se existem as variáveis de sessão necessárias
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_module' not in st.session_state:
        st.session_state.current_module = None

    # Redirecionar para a tela de login se não estiver logado
    if not st.session_state.logged_in:
        login_screen(user_service)
    else:
        selected_module = menu()
        
        if selected_module:
            st.session_state.current_module = selected_module
        
        # Redirecionar para o módulo selecionado
        if st.session_state.current_module == "Estoque":
            estoque_main(key="estoque")
        elif st.session_state.current_module == "Cobrança":
            boletos_main(key="boletos")
        elif st.session_state.current_module == "Financeiro":
            extratos_main(key="extratos")
        elif st.session_state.current_module == "Vendas":
            vendas_main(key="vendas")  # Chamada da função main do arquivo vendas.py

if __name__ == "__main__":
    main()