"""
Sistema de tema simples para SGR
"""
import streamlit as st


def apply_theme():
    """Aplica tema customizado para SGR"""
    st.markdown(
        """
    <style>
        /* Importação da fonte Roboto */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
        
        /* Aplicação global da fonte Roboto */
        * {
            font-family: 'Roboto', sans-serif !important;
        }
        
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif !important;
        }
        
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1.5rem;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1E88E5;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #6c757d;
            margin-top: 0.5rem;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .filter-section {
            background-color: #f1f3f5;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .chart-container {
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #1e88e5, #1976d2);
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: 600;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #1976d2, #1565c0);
            transform: translateY(-2px);
        }
        
        .success-message {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
            padding: 0.75rem 1.25rem;
            border-radius: 0.375rem;
            border: 1px solid;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .error-message {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
            padding: 0.75rem 1.25rem;
            border-radius: 0.375rem;
            border: 1px solid;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .warning-message {
            background-color: #fff3cd;
            border-color: #ffeaa7;
            color: #856404;
            padding: 0.75rem 1.25rem;
            border-radius: 0.375rem;
            border: 1px solid;
            font-family: 'Roboto', sans-serif !important;
        }
        
        .info-message {
            background-color: #d1ecf1;
            border-color: #bee5eb;
            color: #0c5460;
            padding: 0.75rem 1.25rem;
            border-radius: 0.375rem;
            border: 1px solid;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Customização do sidebar */
        .css-1d391kg {
            background-color: #f8f9fa;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Aplicação global da fonte Roboto nos componentes Streamlit */
        .stSelectbox label, .stMultiselect label, .stTextInput label, 
        .stNumberInput label, .stTextArea label, .stDateInput label,
        .stTimeInput label, .stFileUploader label, .stColorPicker label,
        .stSlider label, .stRadio label, .stCheckbox label {
            font-family: 'Roboto', sans-serif !important;
            font-weight: 500 !important;
        }
        
        .stSelectbox div, .stMultiselect div, .stTextInput div, 
        .stNumberInput div, .stTextArea div, .stDateInput div,
        .stTimeInput div, .stFileUploader div, .stColorPicker div,
        .stSlider div, .stRadio div, .stCheckbox div {
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Títulos e headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Markdown e texto geral */
        .stMarkdown, .stText, p, span, div {
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Tabelas */
        .stDataFrame, .stDataFrame table, .stDataFrame th, .stDataFrame td {
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Customização das métricas do Streamlit */
        .css-1xarl3l {
            color: #1E88E5;
        }
        
        /* Estilização avançada das métricas - valores mais escuros */
        [data-testid="metric-container"] {
            font-family: 'Roboto', sans-serif !important;
        }
        
        [data-testid="metric-container"] > div:first-child {
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #495057 !important;  /* Cor mais escura para labels */
            font-family: 'Roboto', sans-serif !important;
        }
        
        [data-testid="metric-container"] > div:nth-child(2) {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #212529 !important;  /* Cor muito mais escura para valores */
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Métrica com delta */
        [data-testid="metric-container"] > div:last-child {
            font-weight: 600 !important;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Labels de métrica mais escuros */
        div[data-testid="metric-container"] div[data-testid="stMarkdownContainer"] p {
            font-weight: 600 !important;
            color: #343a40 !important;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Valores de métrica mais escuros e com Roboto */
        .metric-value, .css-1xarl3l {
            font-weight: 900 !important;
            color: #000000 !important;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* Customização dos gráficos */
        .js-plotly-plot {
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            font-family: 'Roboto', sans-serif !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


class ThemeColors:
    """Constantes de cores do tema"""

    PRIMARY = "#1E88E5"
    PRIMARY_DARK = "#1976D2"
    PRIMARY_LIGHT = "#64B5F6"

    SUCCESS = "#4CAF50"
    WARNING = "#FF9800"
    ERROR = "#F44336"
    INFO = "#2196F3"

    BACKGROUND = "#FFFFFF"
    BACKGROUND_LIGHT = "#F8F9FA"
    TEXT = "#212529"
    TEXT_MUTED = "#6C757D"


def get_color_palette():
    """Retorna paleta de cores para gráficos"""
    return [
        ThemeColors.PRIMARY,
        ThemeColors.SUCCESS,
        ThemeColors.WARNING,
        ThemeColors.ERROR,
        ThemeColors.INFO,
        "#9C27B0",  # Purple
        "#FF5722",  # Deep Orange
        "#607D8B",  # Blue Grey
    ]
