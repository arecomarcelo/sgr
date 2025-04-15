# login.py
import streamlit as st

def login_screen(user_service):
    """
    Tela de login do aplicativo
    """
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
            st.rerun()  # Recarrega a página para atualizar o estado
        else:
            st.error("Usuário ou senha incorretos.")