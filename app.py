import os
import django
import streamlit as st
import time
import requests
import threading

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
from vendas import main as vendas_main
from clientes import main as clientes_main

# Instanciar DataService e UserService
data_service = AppDataService()  # Renomeado para evitar conflito com o DataService de vendas
user_service = UserService(data_service)

# Função para fazer requisições periódicas (keep-alive)
def keep_alive():
    while True:
        try:
            # Faz uma requisição para o próprio servidor
            requests.get("https://oficialsport.streamlit.app/")  # Substitua pela URL da sua aplicação
            st.write("Requisição keep-alive enviada.")
        except Exception as e:
            st.write(f"Erro ao enviar requisição keep-alive: {e}")
        time.sleep(300)  # Espera 5 minutos antes de fazer a próxima requisição

# Inicia a thread de keep-alive
thread = threading.Thread(target=keep_alive)
thread.daemon = True  # A thread será encerrada quando o programa principal terminar
thread.start()

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
            vendas_main(key="vendas")
        elif st.session_state.current_module == "Relatório de Clientes":
            clientes_main(key="clientes")


if __name__ == "__main__":
    main()