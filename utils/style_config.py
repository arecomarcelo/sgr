class StyleConfig:
    """
    Classe responsável por gerenciar as configurações de estilo da aplicação
    """

    @staticmethod
    def get_hide_streamlit_elements():
        """
        Retorna o CSS para ocultar elementos padrão do Streamlit
        """
        return """
            <style>
            #MainMenu {visibility: hidden;} 
            footer {visibility: hidden;} 
            header {visibility: hidden;} 
            .stDeployButton {visibility: hidden;}
            [data-testid="stStatusWidget"] {visibility: hidden;}
            </style>
        """
