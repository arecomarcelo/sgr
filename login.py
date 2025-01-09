# login.py
import streamlit as st

def login_screen(user_service):
  
    # Configurar a página antes de qualquer elemento ser carregado
    st.set_page_config(
        page_title="SGR",
        layout="wide",
        # initial_sidebar_state="collapsed"
    )

    # CSS para ajustar a largura da tela de login
    login_style = """
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;} 
    .stDeployButton {visibility: hidden;}
    [data-testid="stStatusWidget"] {visibility: hidden;}        
    [data-testid="stAppViewContainer"] {
        max-width: 500px; /* Ajuste a largura desejada */
        margin: auto; /* Centraliza o conteúdo */
        padding: 20px; /* Espaço interno */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Efeito de sombra */
        border-radius: 10px; /* Bordas arredondadas */
    }
    </style>
    """

    # Aplicar o CSS
    st.markdown(login_style, unsafe_allow_html=True)

    # Conteúdo da tela de login
    # st.subheader("Sistema de Gerenciamento de Relatórios")
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        # Captura as permissões ao validar o usuário
        is_valid, permissions = user_service.validate_user(username, password)
        if is_valid:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.permissions = permissions  # Armazenar permissões na sessão
            st.success("Login bem-sucedido!")
            
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")


    # # Exibir permissões se o usuário estiver logado
    # if st.session_state.get('logged_in'):
    #     print("Entrou")
    #     st.subheader("Permissões do Usuário")
    #     if st.session_state.get('permissions'):
    #         for perm in st.session_state.permissions:
    #             st.write(f"- {perm}")  # Listar permissões
    #     else:
    #         st.write("Nenhuma permissão encontrada.")
