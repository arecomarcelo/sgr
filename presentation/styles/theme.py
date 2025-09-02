"""
Sistema de temas e estilos para SGR
Centraliza configurações de aparência da aplicação
"""
from enum import Enum
from typing import Any, Dict

import streamlit as st


class ThemeMode(Enum):
    """Modos de tema disponíveis"""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class ColorScheme:
    """Esquema de cores da aplicação"""

    # Cores primárias
    PRIMARY = "#1e88e5"
    PRIMARY_DARK = "#1976d2"
    PRIMARY_LIGHT = "#42a5f5"

    # Cores secundárias
    SECONDARY = "#26a69a"
    SECONDARY_DARK = "#00695c"
    SECONDARY_LIGHT = "#4db6ac"

    # Cores de estado
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    INFO = "#2196f3"

    # Cores neutras
    GRAY_50 = "#fafafa"
    GRAY_100 = "#f5f5f5"
    GRAY_200 = "#eeeeee"
    GRAY_300 = "#e0e0e0"
    GRAY_400 = "#bdbdbd"
    GRAY_500 = "#9e9e9e"
    GRAY_600 = "#757575"
    GRAY_700 = "#616161"
    GRAY_800 = "#424242"
    GRAY_900 = "#212121"

    # Backgrounds
    BACKGROUND_LIGHT = "#ffffff"
    BACKGROUND_DARK = "#1e1e1e"
    SURFACE_LIGHT = "#f8f9fa"
    SURFACE_DARK = "#2d2d2d"


class StyleManager:
    """Gerenciador de estilos da aplicação"""

    def __init__(self):
        self.current_theme = ThemeMode.LIGHT
        self._custom_css_rules: Dict[str, str] = {}

    def apply_global_styles(self):
        """Aplica estilos globais da aplicação"""
        css = self._build_global_css()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    def hide_streamlit_elements(self):
        """Oculta elementos padrão do Streamlit"""
        css = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        [data-testid="stStatusWidget"] {visibility: hidden;}
        .stDecoration {display: none;}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def apply_login_styles(self):
        """Aplica estilos específicos para tela de login"""
        css = f"""
        <style>
        .login-container {{
            max-width: 450px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: linear-gradient(135deg, {ColorScheme.GRAY_50} 0%, {ColorScheme.BACKGROUND_LIGHT} 100%);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid {ColorScheme.GRAY_200};
        }}
        
        .login-header {{
            text-align: center;
            margin-bottom: 2rem;
            color: {ColorScheme.GRAY_800};
        }}
        
        .login-form .stButton > button {{
            background: linear-gradient(135deg, {ColorScheme.PRIMARY} 0%, {ColorScheme.PRIMARY_DARK} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            height: 3rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
        }}
        
        .login-form .stButton > button:hover {{
            background: linear-gradient(135deg, {ColorScheme.PRIMARY_DARK} 0%, {ColorScheme.PRIMARY} 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
        }}
        
        .stTextInput > div > div > input {{
            border-radius: 8px;
            border: 2px solid {ColorScheme.GRAY_300};
            padding: 0.75rem;
            font-size: 1rem;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {ColorScheme.PRIMARY};
            box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def apply_dashboard_styles(self):
        """Aplica estilos para dashboard/relatórios"""
        css = f"""
        <style>
        .dashboard-container {{
            padding: 1rem;
            background-color: {ColorScheme.SURFACE_LIGHT};
            border-radius: 10px;
            margin-bottom: 1rem;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, {ColorScheme.BACKGROUND_LIGHT} 0%, {ColorScheme.GRAY_50} 100%);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid {ColorScheme.GRAY_200};
            text-align: center;
            transition: transform 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {ColorScheme.PRIMARY};
            margin: 0.5rem 0;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: {ColorScheme.GRAY_600};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .data-grid-container {{
            background-color: {ColorScheme.BACKGROUND_LIGHT};
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }}
        
        .filter-section {{
            background-color: {ColorScheme.GRAY_50};
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid {ColorScheme.GRAY_200};
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def apply_form_styles(self):
        """Aplica estilos para formulários"""
        css = f"""
        <style>
        .form-container {{
            background-color: {ColorScheme.BACKGROUND_LIGHT};
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid {ColorScheme.GRAY_200};
        }}
        
        .form-section {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {ColorScheme.GRAY_200};
        }}
        
        .form-section:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        
        .form-title {{
            color: {ColorScheme.GRAY_800};
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        .stButton > button {{
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .primary-button {{
            background-color: {ColorScheme.PRIMARY};
            color: white;
            border: none;
        }}
        
        .primary-button:hover {{
            background-color: {ColorScheme.PRIMARY_DARK};
            transform: translateY(-1px);
        }}
        
        .secondary-button {{
            background-color: {ColorScheme.GRAY_100};
            color: {ColorScheme.GRAY_700};
            border: 1px solid {ColorScheme.GRAY_300};
        }}
        
        .secondary-button:hover {{
            background-color: {ColorScheme.GRAY_200};
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def apply_sidebar_styles(self):
        """Aplica estilos para sidebar"""
        css = f"""
        <style>
        .css-1d391kg {{
            background-color: {ColorScheme.SURFACE_LIGHT};
        }}
        
        .sidebar-title {{
            color: {ColorScheme.GRAY_800};
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
            padding: 1rem 0;
            border-bottom: 2px solid {ColorScheme.PRIMARY};
        }}
        
        .sidebar-menu-item {{
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 8px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .sidebar-menu-item:hover {{
            background-color: {ColorScheme.PRIMARY_LIGHT};
            color: white;
            transform: translateX(4px);
        }}
        
        .sidebar-menu-item.active {{
            background-color: {ColorScheme.PRIMARY};
            color: white;
            font-weight: 600;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def _build_global_css(self) -> str:
        """Constrói CSS global da aplicação"""
        css = f"""
        /* Reset e configurações básicas */
        * {{
            box-sizing: border-box;
        }}
        
        .main-container {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: {ColorScheme.GRAY_800};
            line-height: 1.6;
        }}
        
        /* Títulos e cabeçalhos */
        h1, h2, h3, h4, h5, h6 {{
            color: {ColorScheme.GRAY_800};
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, {ColorScheme.PRIMARY}, {ColorScheme.PRIMARY_DARK});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            font-size: 2rem;
            color: {ColorScheme.PRIMARY};
        }}
        
        /* Cards e containers */
        .card {{
            background-color: {ColorScheme.BACKGROUND_LIGHT};
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid {ColorScheme.GRAY_200};
        }}
        
        /* Alertas e notificações */
        .alert-success {{
            background-color: {ColorScheme.SUCCESS};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        .alert-warning {{
            background-color: {ColorScheme.WARNING};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        .alert-error {{
            background-color: {ColorScheme.ERROR};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        .alert-info {{
            background-color: {ColorScheme.INFO};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        /* Animações */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}
        
        /* Customizações do Streamlit */
        .stApp {{
            background-color: {ColorScheme.SURFACE_LIGHT};
        }}
        
        .stSelectbox > div > div {{
            border-radius: 8px;
        }}
        
        .stDateInput > div > div {{
            border-radius: 8px;
        }}
        
        .stNumberInput > div > div {{
            border-radius: 8px;
        }}
        
        .stTextArea > div > div {{
            border-radius: 8px;
        }}
        
        /* Responsividade */
        @media (max-width: 768px) {{
            .main-container {{
                padding: 0.5rem;
            }}
            
            .card {{
                padding: 1rem;
                margin-bottom: 0.5rem;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            h2 {{
                font-size: 1.5rem;
            }}
        }}
        
        /* Adicionais customizados */
        {self._build_custom_css()}
        """

        return css

    def _build_custom_css(self) -> str:
        """Constrói CSS customizado adicionado dinamicamente"""
        return "\n".join(self._custom_css_rules.values())

    def add_custom_css(self, name: str, css: str):
        """Adiciona regra CSS customizada"""
        self._custom_css_rules[name] = css

    def remove_custom_css(self, name: str):
        """Remove regra CSS customizada"""
        if name in self._custom_css_rules:
            del self._custom_css_rules[name]

    def set_theme(self, theme: ThemeMode):
        """Define o tema da aplicação"""
        self.current_theme = theme
        # Implementar lógica de mudança de tema se necessário


# Instância global do gerenciador de estilos
style_manager = StyleManager()


# Funções de conveniência
def apply_page_style(page_type: str = "dashboard"):
    """
    Aplica estilo para um tipo de página específico

    Args:
        page_type: Tipo da página ('login', 'dashboard', 'form', etc.)
    """
    style_manager.hide_streamlit_elements()
    style_manager.apply_global_styles()

    if page_type == "login":
        style_manager.apply_login_styles()
    elif page_type == "dashboard":
        style_manager.apply_dashboard_styles()
        style_manager.apply_sidebar_styles()
    elif page_type == "form":
        style_manager.apply_form_styles()
        style_manager.apply_sidebar_styles()
    else:
        style_manager.apply_dashboard_styles()
        style_manager.apply_sidebar_styles()


def show_loading_animation():
    """Mostra animação de carregamento"""
    css = """
    <style>
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #e3e3e3;
        border-top: 4px solid #1e88e5;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <div class="loading-container">
        <div class="spinner"></div>
    </div>
    """
    return st.markdown(css, unsafe_allow_html=True)
