# modules.py
import streamlit as st
from style_utils import apply_default_style

def menu():
    # Aplica o estilo padrão
    apply_default_style()     
    st.sidebar.title("Menu Principal")
    
    # Definindo os módulos e suas permissões necessárias
    module_permissions = {
        "Estoque": "view_produtos",
        "Cobrança": "view_boletos",
        "Financeiro": "view_extratos",
        "Vendas": "view_venda"
    }
    
    # Módulos disponíveis
    modules = ["", "Sair"]  # Sempre incluir a opção de sair

    # Verificar permissões e adicionar módulos disponíveis
    for module, permission in module_permissions.items():
        if permission in st.session_state.permissions or st.session_state.username == 'admin':
            modules.insert(-1, module)  # Adiciona antes da opção "Sair"

    # print(st.session_state.permissions)  # Para depuração, pode ser removido depois
    
    selected = st.sidebar.selectbox(
        "Selecione um módulo",
        modules
    )
    
    if selected == "Sair":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_module = None

        st.success("Você saiu com sucesso.")
        st.rerun()
    
    elif selected:
        st.session_state.current_module = selected

    return selected