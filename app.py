import logging
import os
import threading
import time
from datetime import date, datetime

import django

import pandas as pd
import requests
import streamlit as st

# Configuração da página (DEVE SER A PRIMEIRA COISA NO SCRIPT)
st.set_page_config(
    page_title="SGR", page_icon="📊", layout="wide", initial_sidebar_state="expanded"
)

# Configurações para prevenir hibernação
if "session_started" not in st.session_state:
    st.session_state["session_started"] = True
    st.session_state["last_activity"] = time.time()

# Auto-refresh para manter sessão ativa
if time.time() - st.session_state.get("last_activity", 0) > 240:  # 4 minutos
    st.session_state["last_activity"] = time.time()
    st.rerun()

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from apps.auth.modules import menu
from apps.auth.views import login_screen
from apps.boletos.views import main as boletos_main
from apps.clientes.views import main as clientes_main
from apps.estoque.views import main as estoque_main
from apps.extratos.views import main as extratos_main
from apps.vendas.views import main as vendas_main

# Importações após a configuração da página
from service import DataService as AppDataService
from service import UserService

# Importações da aplicação de vendas refatorada
try:
    from core.container_vendas import DIContainer
    from core.exceptions import BusinessLogicError, SGRException, ValidationError
    from domain.services.vendas_service import VendasService
    from presentation.components.data_grid_simple import DataGrid
    from presentation.components.forms_vendas import (
        FilterForm,
        LoadingHelper,
        MetricsDisplay,
        ValidationHelper,
    )
    from presentation.styles.theme_simple import apply_theme

    VENDAS_REFATORADO_AVAILABLE = True
except ImportError as e:
    VENDAS_REFATORADO_AVAILABLE = False

# Instanciar DataService e UserService
data_service = (
    AppDataService()
)  # Renomeado para evitar conflito com o DataService de vendas
user_service = UserService(data_service)

# Instanciar serviços de vendas
if VENDAS_REFATORADO_AVAILABLE:
    container = DIContainer()
    vendas_service = container.get_vendas_service()
    logger = logging.getLogger(__name__)


# Função para fazer requisições periódicas (keep-alive) - REMOVIDO PROBLEMA DE SCRIPT CONTEXT
def keep_alive():
    """
    Keep-alive em background sem problemas de ScriptRunContext
    Usa apenas requests, sem interação com Streamlit
    """
    import logging
    import time

    import requests

    # Configurar logger específico para keep-alive
    keep_alive_logger = logging.getLogger("keep_alive")
    keep_alive_logger.setLevel(logging.INFO)

    while True:
        try:
            # Fazer requisição silenciosa apenas para manter vivo
            # Não usar st.write aqui para evitar ScriptRunContext warnings
            response = requests.get("https://oficialsport.streamlit.app/", timeout=10)
            keep_alive_logger.info(
                f"Keep-alive enviado - Status: {response.status_code}"
            )
        except Exception as e:
            keep_alive_logger.warning(f"Erro no keep-alive: {e}")
        time.sleep(300)  # 5 minutos


# Verificar se deve inicializar keep-alive (apenas uma vez por sessão)
if "keep_alive_started" not in st.session_state:
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    st.session_state["keep_alive_started"] = True


def _show_manual_dialog():
    """
    Exibe o manual em uma janela de diálogo
    """
    try:
        # Ler o conteúdo do manual
        manual_path = "documentacao/Manual_Relatorio_Vendas.md"
        
        with open(manual_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        
        # Usar st.expander para simular uma janela separada
        with st.expander("📖 Manual do Relatório de Vendas", expanded=True):
            # Converter markdown para HTML com melhor formatação
            html_content = _convert_markdown_to_html(markdown_content)
            st.markdown(html_content, unsafe_allow_html=True)
            
            # Adicionar botão para fechar
            if st.button("❌ Fechar Manual"):
                st.rerun()
                
    except FileNotFoundError:
        st.error("❌ Manual não encontrado. Verifique se o arquivo existe.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar o manual: {str(e)}")


def _convert_markdown_to_html(markdown_content):
    """
    Converte markdown para HTML com melhor formatação para Streamlit
    """
    # Importar biblioteca markdown se disponível, senão usar formatação básica
    try:
        import markdown
        html = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
        return f"""
        <div style="
            font-family: 'Roboto', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-height: 600px;
            overflow-y: auto;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        ">
            {html}
        </div>
        """
    except ImportError:
        # Se não tiver markdown, usar formatação básica
        return _basic_markdown_to_html(markdown_content)


def _basic_markdown_to_html(content):
    """
    Conversão básica de markdown para HTML
    """
    # Substituições básicas para formatação
    content = content.replace('\n# ', '\n<h1>')
    content = content.replace('\n## ', '\n<h2>')
    content = content.replace('\n### ', '\n<h3>')
    content = content.replace('\n#### ', '\n<h4>')
    content = content.replace('\n', '<br>')
    content = content.replace('**', '<strong>').replace('**', '</strong>')
    content = content.replace('*', '<em>').replace('*', '</em>')
    content = content.replace('`', '<code>').replace('`', '</code>')
    
    return f"""
    <div style="
        font-family: 'Roboto', Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    ">
        {content}
    </div>
    """


def vendas_dashboard():
    """
    Dashboard de vendas integrado
    """
    try:
        # Aplicar tema
        apply_theme()

        # Header
        st.markdown(
            "<h1 style='text-align: center; color: #1E88E5;'>📊 SGR - Dashboard de Vendas</h1>",
            unsafe_allow_html=True,
        )
        
        # Botão Ler Manual centralizado abaixo do título
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📖 Ler Manual", type="secondary", use_container_width=True):
                # Importar e executar o servidor do manual
                try:
                    from manual_server import open_manual_in_browser
                    open_manual_in_browser()
                    st.success("✅ Manual aberto no navegador!")
                except Exception as e:
                    st.error(f"❌ Erro ao abrir manual: {str(e)}")
                    st.info("💡 Verifique se seu navegador permite pop-ups ou acesse manualmente: http://localhost:8888/manual")
        
        st.markdown("---")

        # Renderizar seções
        _render_update_info()
        _render_filters_and_metrics()
        _render_download_section()
        _render_charts()
        _render_data_grid()

    except SGRException as e:
        logger.error(f"SGR Error: {str(e)}")
        st.error(f"Erro na aplicação: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error("Erro inesperado na aplicação. Verifique os logs.")


def _render_update_info():
    """Renderiza informações de atualização"""
    st.subheader("🔄 Informações de Atualização")

    try:
        info = vendas_service.get_informacoes_atualizacao()

        with st.expander("Dados da Última Sincronização", expanded=True):
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown(
                    f"""
                <div style='
                    background: #ffffff; 
                    border-radius: 10px; 
                    padding: 16px; 
                    text-align: center; 
                    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
                    font-family: Roboto, sans-serif;
                '>
                    <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>📅 Data</div>
                    <div style='font-size: 1.4rem; font-weight: 700; color: #1E88E5;'>{info['data']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                <div style='
                    background: #ffffff; 
                    border-radius: 10px; 
                    padding: 16px; 
                    text-align: center; 
                    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
                    font-family: Roboto, sans-serif;
                '>
                    <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>⏰ Hora</div>
                    <div style='font-size: 1.4rem; font-weight: 700; color: #1E88E5;'>{info['hora']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                <div style='
                    background: #ffffff; 
                    border-radius: 10px; 
                    padding: 16px; 
                    text-align: center; 
                    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
                    font-family: Roboto, sans-serif;
                    min-height: 90px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                '>
                    <div style='font-size: 0.8rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>📊 Período</div>
                    <div style='font-size: 1.1rem; font-weight: 700; color: #1E88E5;'>{info['periodo']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col4:
                st.markdown(
                    f"""
                <div style='
                    background: #ffffff; 
                    border-radius: 10px; 
                    padding: 16px; 
                    text-align: center; 
                    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
                    font-family: Roboto, sans-serif;
                '>
                    <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>✅ Inseridos</div>
                    <div style='font-size: 1.4rem; font-weight: 700; color: #1E88E5;'>{info['inseridos']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col5:
                st.markdown(
                    f"""
                <div style='
                    background: #ffffff; 
                    border-radius: 10px; 
                    padding: 16px; 
                    text-align: center; 
                    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
                    font-family: Roboto, sans-serif;
                '>
                    <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>🔄 Atualizados</div>
                    <div style='font-size: 1.4rem; font-weight: 700; color: #1E88E5;'>{info['atualizados']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    except Exception as e:
        logger.warning(f"Could not load update info: {str(e)}")
        st.warning("Informações de atualização indisponíveis")


def _render_metrics_cards(metrics):
    """Renderiza métricas em cards no mesmo estilo das Informações de Atualização"""
    if not metrics:
        st.info("Nenhuma métrica disponível")
        return

    # Função auxiliar para formatar moeda
    def format_currency(value):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Primeira linha: Total Entradas, Total Parcelado, Valor Total
    col1, col2, col3 = st.columns(3)

    with col1:
        entradas = metrics.get("total_entradas", 0)
        valor_formatado = format_currency(entradas)
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>💰 Total Entradas</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{valor_formatado}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        parcelado = metrics.get("total_parcelado", 0)
        parcelado_formatado = format_currency(parcelado)
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>⏳ Total Parcelado</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{parcelado_formatado}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        total_valor = metrics.get("total_valor", 0)
        total_formatado = format_currency(total_valor)
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>💎 Valor Total</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{total_formatado}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Segunda linha: Total de Vendas, Ticket Médio, Margem Média
    col4, col5, col6 = st.columns(3)

    with col4:
        total_quantidade = metrics.get("total_quantidade", 0)
        quantidade_formatada = f"{total_quantidade:,}".replace(",", ".")
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>📊 Total de Vendas</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{quantidade_formatada}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col5:
        ticket_medio = metrics.get("ticket_medio", 0)
        ticket_formatado = format_currency(ticket_medio)
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>🎯 Ticket Médio</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{ticket_formatado}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col6:
        margem_media = metrics.get("margem_media", 0)
        margem_texto = f"{margem_media:.1f}%" if margem_media > 0 else "N/A"
        st.markdown(
            f"""
        <div style='
            background: #ffffff; 
            border-radius: 10px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.15);
            font-family: Roboto, sans-serif;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 0.9rem; color: #1E88E5; margin-bottom: 8px; font-weight: 600;'>📈 Margem Média</div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1E88E5;'>{margem_texto}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def _render_vendedores_com_fotos(vendas_por_vendedor):
    """Renderiza todos os vendedores da tabela com suas fotos em cards 5x2"""
    import base64
    import os
    from io import BytesIO

    import pandas as pd
    from PIL import Image

    # Lista completa de vendedores da tabela Vendedores (ordem das fotos)
    vendedores_tabela = [
        {"nome": "Noé Dutra", "foto": "1"},
        {"nome": "Nilton Jonas Gonçalves de Moraes", "foto": "2"},
        {"nome": "César Henrique Rodrigues", "foto": "3"},
        {"nome": "Rocha Jr.", "foto": "4"},
        {"nome": "Diney Scalabrini", "foto": "5"},
        {"nome": "João Paulo", "foto": "6"},
        {"nome": "Lauro Jarbas de Oliveira", "foto": "7"},
        {"nome": "Giovana Lelis", "foto": "8"},
        {"nome": "Carlos Gabriel Carvalho Macedo", "foto": "9"},
        {"nome": "Cássio Gadagnoto", "foto": "10"},
    ]

    # Criar dicionário de vendas existentes para consulta rápida
    vendas_dict = {}
    total_geral = 0

    if vendas_por_vendedor is not None and not vendas_por_vendedor.empty:
        total_geral = float(vendas_por_vendedor["total_valor"].sum())
        for _, row in vendas_por_vendedor.iterrows():
            vendas_dict[row["VendedorNome"]] = {
                "total_valor": float(row["total_valor"]),
                "percentual": (float(row["total_valor"]) / total_geral * 100)
                if total_geral > 0
                else 0,
            }

    # Preparar dados completos dos vendedores
    vendedores_completos = []
    for vendedor in vendedores_tabela:
        nome = vendedor["nome"]
        if nome in vendas_dict:
            # Vendedor com vendas
            vendedores_completos.append(
                {
                    "nome": nome,
                    "foto": vendedor["foto"],
                    "total_valor": vendas_dict[nome]["total_valor"],
                    "percentual": vendas_dict[nome]["percentual"],
                }
            )
        else:
            # Vendedor sem vendas (zerado)
            vendedores_completos.append(
                {
                    "nome": nome,
                    "foto": vendedor["foto"],
                    "total_valor": 0.0,
                    "percentual": 0.0,
                }
            )

    # Ordenar vendedores por volume de vendas (maior para menor)
    vendedores_ordenados = sorted(
        vendedores_completos, key=lambda x: x["total_valor"], reverse=True
    )

    # Função para converter imagem em base64 mantendo transparência
    def get_image_base64(image_path, size=(80, 80)):
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)

                # Manter transparência se for PNG
                if img.mode in ("RGBA", "LA") or (
                    img.mode == "P" and "transparency" in img.info
                ):
                    # Para PNG com transparência, manter o canal alfa
                    img = img.convert("RGBA")
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                else:
                    # Para outros formatos, converter para RGB
                    img = img.convert("RGB")
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")

                img_str = base64.b64encode(buffered.getvalue()).decode()
                return f"data:image/png;base64,{img_str}"
            else:
                return None
        except Exception as e:
            return None

    # Função para formatar moeda
    def format_currency(value):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Renderizar cards dos vendedores em layout 5x2 (5 por linha, 2 linhas)
    # Primeira linha (vendedores 1-5)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols_linha1 = [col1, col2, col3, col4, col5]

    for i in range(5):  # Primeira linha
        if i < len(vendedores_ordenados):
            vendedor = vendedores_ordenados[i]
            _render_card_vendedor(
                cols_linha1[i], vendedor, get_image_base64, format_currency
            )

    # Segunda linha (vendedores 6-10)
    col6, col7, col8, col9, col10 = st.columns(5)
    cols_linha2 = [col6, col7, col8, col9, col10]

    for i in range(5):  # Segunda linha
        idx = i + 5
        if idx < len(vendedores_ordenados):
            vendedor = vendedores_ordenados[idx]
            _render_card_vendedor(
                cols_linha2[i], vendedor, get_image_base64, format_currency
            )


def _render_card_vendedor(col, vendedor, get_image_base64, format_currency):
    """Renderiza um card individual do vendedor"""
    with col:
        # Buscar foto do vendedor
        foto_path_jpg = f"fotos/{vendedor['foto']}.jpg"
        foto_path_png = f"fotos/{vendedor['foto']}.png"

        # Usar JPG se existir, senão PNG
        foto_path = foto_path_jpg if os.path.exists(foto_path_jpg) else foto_path_png
        image_b64 = get_image_base64(foto_path)

        if image_b64:
            # Com foto
            st.markdown(
                f"""
            <div style='
                background: #ffffff; 
                border-radius: 15px; 
                padding: 20px; 
                text-align: center; 
                box-shadow: 0 6px 16px rgba(30, 136, 229, 0.2);
                font-family: Roboto, sans-serif;
                margin-bottom: 20px;
                border: 2px solid #E3F2FD;
            '>
                <img src="{image_b64}" style="
                    width: 80px; 
                    height: 80px; 
                    margin-bottom: 12px;
                    object-fit: cover;
                ">
                <div style='font-size: 0.9rem; color: #1E88E5; font-weight: 600; margin-bottom: 8px;'>
                    {vendedor['nome']}
                </div>
                <div style='font-size: 1.1rem; font-weight: 700; color: #1565C0; margin-bottom: 6px;'>
                    {format_currency(vendedor['total_valor'])}
                </div>
                <div style='
                    background: #1E88E5; 
                    color: white; 
                    padding: 4px 12px; 
                    border-radius: 20px; 
                    font-size: 0.8rem; 
                    font-weight: 600;
                    display: inline-block;
                '>
                    {vendedor['percentual']:.1f}%
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            # Sem foto - usar avatar com iniciais
            iniciais = "".join(
                [nome[0] for nome in vendedor["nome"].split()[:2]]
            ).upper()
            st.markdown(
                f"""
            <div style='
                background: #ffffff; 
                border-radius: 15px; 
                padding: 20px; 
                text-align: center; 
                box-shadow: 0 6px 16px rgba(30, 136, 229, 0.2);
                font-family: Roboto, sans-serif;
                margin-bottom: 20px;
                border: 2px solid #E3F2FD;
            '>
                <div style="
                    width: 80px; 
                    height: 80px; 
                    border-radius: 50%; 
                    background: linear-gradient(135deg, #1E88E5, #1565C0);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    font-weight: 700;
                    margin: 0 auto 12px auto;
                    border: 3px solid #1E88E5;
                ">
                    {iniciais}
                </div>
                <div style='font-size: 0.9rem; color: #1E88E5; font-weight: 600; margin-bottom: 8px;'>
                    {vendedor['nome']}
                </div>
                <div style='font-size: 1.1rem; font-weight: 700; color: #1565C0; margin-bottom: 6px;'>
                    {format_currency(vendedor['total_valor'])}
                </div>
                <div style='
                    background: #1E88E5; 
                    color: white; 
                    padding: 4px 12px; 
                    border-radius: 20px; 
                    font-size: 0.8rem; 
                    font-weight: 600;
                    display: inline-block;
                '>
                    {vendedor['percentual']:.1f}%
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def _render_filters_and_metrics():
    """Renderiza filtros e métricas"""
    st.subheader("🔍 Filtros")

    # Inicializar dados do mês atual no primeiro carregamento
    if "df_vendas" not in st.session_state or st.session_state["df_vendas"] is None:
        _load_initial_data()

    # Filtros
    with st.expander("🔍 Filtros de Data e Vendedor", expanded=True):
        filter_form = FilterForm()

        # Obter listas para filtros
        try:
            loading = LoadingHelper.show_loading("Carregando opções de filtros...")
            vendedores = vendas_service.get_vendedores_ativos()
            situacoes = vendas_service.get_situacoes_disponiveis()
            LoadingHelper.hide_loading(loading)

            filters = filter_form.render_filters(vendedores, situacoes)

            # Botão para aplicar filtros
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 Aplicar Filtros", type="primary"):
                    _apply_filters(filters)

            with col2:
                if st.button("🔄 Recarregar Dados do Mês"):
                    _load_initial_data()

        except Exception as e:
            LoadingHelper.hide_loading(loading)
            ValidationHelper.show_error(f"Erro ao carregar filtros: {str(e)}")
            return

    # Renderizar métricas se houver dados
    if (
        st.session_state.get("df_vendas") is not None
        and not st.session_state["df_vendas"].empty
    ):
        st.subheader("💎 Métricas de Vendas")
        _render_metrics_cards(st.session_state.get("metricas", {}))


def _load_initial_data():
    """Carrega dados iniciais do mês atual"""
    try:
        # Carregar dados do mês atual por padrão
        loading = LoadingHelper.show_loading("Carregando dados do mês atual...")
        df_vendas = vendas_service.get_vendas_mes_atual()
        LoadingHelper.hide_loading(loading)

        # Calcular métricas
        loading = LoadingHelper.show_loading("Calculando métricas...")
        metricas = vendas_service.get_metricas_vendas(df_vendas)
        LoadingHelper.hide_loading(loading)

        # Armazenar dados na sessão para uso posterior
        st.session_state["df_vendas"] = df_vendas
        st.session_state["metricas"] = metricas

        if df_vendas.empty:
            ValidationHelper.show_warning("Nenhum dado encontrado para o mês atual")

    except Exception as e:
        ValidationHelper.show_error(f"Erro ao carregar dados iniciais: {str(e)}")
        st.session_state["df_vendas"] = pd.DataFrame()
        st.session_state["metricas"] = {}


def _apply_filters(filters):
    """Aplica filtros personalizados"""
    try:
        # Validar filtros se informados
        if filters.get("data_inicio") and filters.get("data_fim"):
            if not ValidationHelper.validate_date_range(
                filters["data_inicio"], filters["data_fim"]
            ):
                return

            # Obter dados filtrados
            loading = LoadingHelper.show_loading("Carregando dados de vendas...")
            df_vendas = vendas_service.get_vendas_filtradas(
                data_inicio=filters["data_inicio"],
                data_fim=filters["data_fim"],
                vendedores=filters["vendedores"] if filters["vendedores"] else None,
                situacoes=filters["situacoes"] if filters["situacoes"] else None,
            )
            LoadingHelper.hide_loading(loading)
        else:
            ValidationHelper.show_error("Por favor, informe as datas de início e fim")
            return

        # Calcular métricas
        loading = LoadingHelper.show_loading("Calculando métricas...")
        metricas = vendas_service.get_metricas_vendas(df_vendas)
        LoadingHelper.hide_loading(loading)

        # Armazenar dados na sessão para uso posterior
        st.session_state["df_vendas"] = df_vendas
        st.session_state["metricas"] = metricas

        if df_vendas.empty:
            ValidationHelper.show_warning(
                "Nenhum dado encontrado para os filtros selecionados"
            )
        else:
            st.rerun()

    except ValidationError as e:
        ValidationHelper.show_error(f"Erro de validação: {str(e)}")
    except BusinessLogicError as e:
        ValidationHelper.show_error(f"Erro de negócio: {str(e)}")
    except Exception as e:
        ValidationHelper.show_error(f"Erro inesperado: {str(e)}")
        logger.error(f"Erro ao aplicar filtros: {str(e)}")


def _render_download_section():
    """Renderiza seção de download dos dados"""
    st.subheader("📥 Download dos Dados")

    # Verificar se há dados disponíveis
    has_data = (
        "df_vendas" in st.session_state
        and st.session_state["df_vendas"] is not None
        and not st.session_state["df_vendas"].empty
    )

    col1, col2, col3 = st.columns(3)

    if has_data:
        df = st.session_state["df_vendas"]

        with col1:
            # Download Excel
            from io import BytesIO

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Vendas", index=False)

            st.download_button(
                label="📊 Download Excel",
                data=buffer.getvalue(),
                file_name=f"vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with col2:
            # Download CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col3:
            st.markdown(
                f"""
            <div style='
                height: 38px; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                background-color: #d1ecf1; 
                border: 1px solid #bee5eb; 
                border-radius: 0.25rem; 
                color: #0c5460; 
                font-weight: 500;
            '>
                📊 {len(df)} registros
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        # Mostrar botões desabilitados se não há dados
        with col1:
            st.button("📊 Download Excel", disabled=True, use_container_width=True)

        with col2:
            st.button("📄 Download CSV", disabled=True, use_container_width=True)

        with col3:
            st.markdown(
                """
            <div style='
                height: 38px; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                background-color: #d1ecf1; 
                border: 1px solid #bee5eb; 
                border-radius: 0.25rem; 
                color: #0c5460; 
                font-weight: 500;
            '>
                📊 Nenhum dado carregado
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("---")


def _render_charts():
    """Renderiza gráficos de análise"""
    if "df_vendas" not in st.session_state or st.session_state["df_vendas"] is None:
        return

    df_vendas = st.session_state["df_vendas"]

    if df_vendas.empty:
        st.warning("Não há dados para exibir gráficos")
        return

    st.subheader("📈 Análise por Vendedor")

    # Obter dados agregados por vendedor
    vendas_por_vendedor = vendas_service.get_vendas_por_vendedor(df_vendas, top_n=10)

    if not vendas_por_vendedor.empty:
        # Primeiro gráfico - Distribuição por Valor (Pizza)
        st.subheader("📊 Distribuição por Valor")
        fig_pie = _create_pie_chart(vendas_por_vendedor)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # Segundo gráfico - Quantidade por Vendedor (Barras)
        st.subheader("📈 Quantidade por Vendedor")
        fig_bar = _create_bar_chart(vendas_por_vendedor)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # Terceiro gráfico - Valor de Vendas por Vendedor com fotos
        st.subheader("💰 Valor de Vendas por Vendedor")
        try:
            _render_vendedores_com_fotos(vendas_por_vendedor)
        except Exception as e:
            logger.error(f"Erro ao renderizar vendedores com fotos: {str(e)}")
            st.error(f"Erro ao exibir vendedores: {str(e)}")

    st.markdown("---")


def _render_data_grid():
    """Renderiza grid de dados"""
    if "df_vendas" not in st.session_state or st.session_state["df_vendas"] is None:
        return

    df_vendas = st.session_state["df_vendas"]

    if df_vendas.empty:
        st.info("Nenhum dado disponível para exibição")
        return

    st.subheader("📋 Dados Detalhados")

    # Usar componente reutilizável
    data_grid = DataGrid()

    # Preparar dados para exibição
    df_display = df_vendas[
        [
            "ClienteNome",
            "VendedorNome",
            "ValorProdutos",
            "ValorDesconto",
            "ValorTotal",
            "Data",
        ]
    ].copy()

    # Formatar valores monetários
    for col in ["ValorProdutos", "ValorDesconto", "ValorTotal"]:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(
                lambda x: vendas_service.formatar_valor_monetario(x)
                if pd.notna(x)
                else ""
            )

    # Renomear colunas
    df_display.columns = [
        "Cliente",
        "Vendedor",
        "Valor Produtos",
        "Desconto",
        "Valor Total",
        "Data",
    ]

    # Renderizar grid
    data_grid.render_data_grid(
        df_display,
        title="Vendas Detalhadas",
        show_download=False,
        filename_prefix="vendas_detalhadas",
    )


def _create_pie_chart(df):
    """Cria gráfico de pizza"""
    import plotly.express as px
    import plotly.graph_objects as go

    # Calcular percentuais
    total = df["total_valor"].sum()
    df["percentual"] = (df["total_valor"] / total * 100).round(1)

    # Definir cores consistentes para cada vendedor
    colors = px.colors.qualitative.Set3[: len(df)]

    # Criar labels customizados com valor e percentual
    labels_customizados = []
    for i, row in df.iterrows():
        valor_formatado = (
            f"R$ {row['total_valor']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        labels_customizados.append(
            f"{row['VendedorNome']}<br>{valor_formatado} ({row['percentual']}%)"
        )

    fig = px.pie(
        df,
        values="total_valor",
        names="VendedorNome",
        title="Distribuição de Vendas por Vendedor (Valor)",
        color_discrete_sequence=px.colors.sequential.Blues,
        hole=0.4,
    )

    fig.update_layout(
        legend_title="Vendedores",
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        margin=dict(t=50, b=50, l=10, r=10),
        height=400,
    )

    return fig


def _create_bar_chart(df):
    """Cria gráfico de barras"""
    import plotly.express as px

    fig = px.bar(
        df,
        x="VendedorNome",
        y="quantidade",
        title="Quantidade de Vendas por Vendedor",
        color="quantidade",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        xaxis_title="Vendedor",
        yaxis_title="Quantidade",
        xaxis_tickangle=-45,
        height=400,
    )

    return fig


def _create_value_percentage_chart(df):
    """Cria gráfico de barras com valor e percentual"""
    try:
        import plotly.express as px

        if df is None or df.empty:
            return None

        if "total_valor" not in df.columns or "VendedorNome" not in df.columns:
            return None

        # Calcular percentuais
        total_geral = float(df["total_valor"].sum())
        if total_geral <= 0:
            return None

        # Preparar dados simples
        df_chart = df.copy()
        df_chart["percentual"] = (df_chart["total_valor"] / total_geral * 100).round(1)

        # Gráfico simples com plotly express
        fig = px.bar(
            df_chart,
            x="VendedorNome",
            y="total_valor",
            title="💰 Valor de Vendas por Vendedor",
            labels={"VendedorNome": "Vendedor", "total_valor": "Valor (R$)"},
            color="total_valor",
            color_continuous_scale="Blues",
        )

        # Customizar layout
        fig.update_layout(
            xaxis_tickangle=-45, height=450, showlegend=False, coloraxis_showscale=False
        )

        # Adicionar texto nas barras com fundo azul escuro
        for i, row in df_chart.iterrows():
            fig.add_annotation(
                x=row["VendedorNome"],
                y=row["total_valor"] / 2,
                text=f"R$ {float(row['total_valor']):,.0f}<br>{row['percentual']:.1f}%".replace(
                    ",", "."
                ),
                showarrow=False,
                font=dict(color="white", size=12, family="Arial Black"),
                bgcolor="#1565C0",
                bordercolor="#0D47A1",
                borderwidth=1,
            )

        return fig

    except Exception:
        return None


def main():
    """
    Função principal do aplicativo
    """
    # Verificar se existem as variáveis de sessão necessárias
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_module" not in st.session_state:
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
        elif st.session_state.current_module == "Relatório de Vendas":
            if VENDAS_REFATORADO_AVAILABLE:
                try:
                    vendas_dashboard()
                except Exception as e:
                    st.error(f"❌ Erro na versão refatorada: {str(e)}")
                    st.info("🔄 Voltando para versão original...")
                    vendas_main(key="vendas")
            else:
                vendas_main(key="vendas")
        elif st.session_state.current_module == "Relatório de Clientes":
            clientes_main(key="clientes")


if __name__ == "__main__":
    main()
