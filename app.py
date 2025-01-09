# main.py
import os
import django
import streamlit as st
from service import UserService, DataService
from modules import menu
from login import login_screen
from estoque import main as estoque_main
from extratos import main as extratos_main


# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Instanciar DataService e UserService
data_service = DataService()
user_service = UserService(data_service)

def main():  
    
          
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_module' not in st.session_state:
        st.session_state.current_module = None

    if not st.session_state.logged_in:
        login_screen(user_service)
    else:
        selected_module = menu()
        
        if selected_module:
            st.session_state.current_module = selected_module
        
        if st.session_state.current_module == "Estoque":
            estoque_main()
        elif st.session_state.current_module == "Cobrança":
            st.title("Módulo de Cobrança")
        elif st.session_state.current_module == "Financeiro":
            extratos_main()

if __name__ == "__main__":
    main()
