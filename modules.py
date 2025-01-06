# # modules.py
# import streamlit as st

# def menu():
#     st.sidebar.title("Menu Principal")
    
#     modules = ["", "Estoque", "Cobrança", "Financeiro", "Sair"]
   
#     print(st.session_state.permissions)
    
#     selected = st.sidebar.selectbox(
#         "Selecione um módulo",
#         modules
#     )
    
#     if selected == "Sair":
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_module = None

#         st.success("Você saiu com sucesso.")
#         st.rerun()
    
#     elif selected:
#         st.session_state.current_module = selected

#     return selected



# modules.py
import streamlit as st

def menu():
    st.sidebar.title("Menu Principal")
    
    # Definindo os módulos e suas permissões necessárias
    module_permissions = {
        "Estoque": "view_produtos",
        "Cobrança": "view_boletos",
        "Financeiro": "view_extratos"
    }
    
    # Módulos disponíveis
    modules = ["", "Sair"]  # Sempre incluir a opção de sair

    # Verificar permissões e adicionar módulos disponíveis
    for module, permission in module_permissions.items():
        if permission in st.session_state.permissions:
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