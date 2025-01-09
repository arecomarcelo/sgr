# estoque.py
import streamlit as st
from service import DataService
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from io import BytesIO
import locale
from style_utils import apply_default_style

# Tentar configurar a localidade
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # st.warning("A localidade 'pt_BR.UTF-8' não está disponível. Usando a localidade padrão.")
    locale.setlocale(locale.LC_ALL, 'C')  # ou 'en_US.UTF-8'

@st.cache_data
def load_data(_service, table_name, fields):
    with st.spinner('Carregando dados...'):
        return _service.get_data(table_name, fields)

def download_excel(df):
    """
    Função para gerar arquivo Excel com formatação adequada
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Formatar números antes de exportar
        df_formatted = df.copy()
        if 'ValorCusto' in df.columns:
            df_formatted['ValorCusto'] = df_formatted['ValorCusto'].apply(
                lambda x: format_currency(x) if pd.notnull(x) else ''
            )
        if 'ValorVenda' in df.columns:
            df_formatted['ValorVenda'] = df_formatted['ValorVenda'].apply(
                lambda x: format_currency(x) if pd.notnull(x) else ''
            )
        if 'EstoqueGalpao' in df.columns:
            df_formatted['EstoqueGalpao'] = df_formatted['EstoqueGalpao'].apply(
                lambda x: format_number(x) if pd.notnull(x) else ''
            )
        
        df_formatted.to_excel(writer, index=False, sheet_name='Relatório')
        
        # Ajustar largura das colunas
        worksheet = writer.sheets['Relatório']
        for idx, col in enumerate(df_formatted.columns):
            max_length = max(
                df_formatted[col].astype(str).apply(len).max(),
                len(str(col))
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
            
    return output.getvalue()

def format_currency(value):
    """
    Função auxiliar para formatar valores monetários
    """
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def format_number(value):
    """
    Função auxiliar para formatar números inteiros
    """
    return locale.format_string("%.0f", value, grouping=True)

def calculate_totals(data):
    # Converter valores para numérico antes de somar
    estoque = pd.to_numeric(data['EstoqueGalpao'], errors='coerce')
    valor_custo = pd.to_numeric(data['ValorCusto'], errors='coerce')
    valor_venda = pd.to_numeric(data['ValorVenda'], errors='coerce')
    
    return {
        'total_produtos': float(estoque.sum()),
        'total_custo': float(valor_custo.sum()),
        'total_venda': float(valor_venda.sum())
    }

def display_totals(totals, df):
    # Criando um container para os totalizadores e botão
    container = st.container()
    
    with container:
        # Dividindo em 5 colunas: 3 para totalizadores, 1 vazia para espaço, 1 para o botão
        col1, col2, col3, col_space, col_button = st.columns([2,2,2,3,1])
        
        with col1:
            st.metric(
                label="Total Produtos",
                value=format_number(totals['total_produtos'])
            )
        with col2:
            st.metric(
                label="Total Custo",
                value=format_currency(totals['total_custo'])
            )
        with col3:
            st.metric(
                label="Total Venda",
                value=format_currency(totals['total_venda'])
            )
        with col_button:
            st.write("")  # Espaço para alinhar verticalmente com as métricas
            if st.download_button(
                label="📥 Baixar Excel",
                data=download_excel(df),
                file_name="relatorio_estoque.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True  # Faz o botão usar a largura total da coluna
            ):
                st.success("Download iniciado!")

def create_grid_options(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        enableCellTextSelection=True,
        suppressRowClickSelection=True,
        enableExcelExport=True,
        enableCsvExport=True,
        onFirstDataRendered='onFirstDataRendered',
        onFilterChanged='onFilterChanged'
    )  

    # Configurações de coluna
    gb.configure_default_column(
        filter=True,
        cellStyle={'border': '1px solid black'},
        floatingFilter=True
    )
    
    # Configuração dos cabeçalhos personalizados
    gb.configure_column("CodigoInterno", headerName="Código Gestão")
    gb.configure_column("CodigoExpedicao", headerName="Código Expedição")
    gb.configure_column("Nome", headerName="Nome")
    gb.configure_column("Descricao", headerName="Descrição")
    gb.configure_column("NomeGrupo", headerName="Grupo")
    gb.configure_column("EstoqueGalpao", 
                       headerName="Estoque",
                       type=["numericColumn", "numberColumnFilter"],
                       valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 0})")
    gb.configure_column("ValorCusto", 
                       headerName="Valor Custo",
                       type=["numericColumn", "numberColumnFilter"],
                       valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})")
    gb.configure_column("ValorVenda", 
                       headerName="Valor Venda",
                       type=["numericColumn", "numberColumnFilter"],
                       valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})")
    gb.configure_column("Localizacao", headerName="Localização")
    
    # Totalizadores
    gb.configure_column("EstoqueGalpao", aggFunc="sum", header_name="Total Estoque")
    gb.configure_column("ValorCusto", aggFunc="sum", header_name="Total Custo")
    gb.configure_column("ValorVenda", aggFunc="sum", header_name="Total Venda")
    
    return gb.build()

def main():
    # # CSS para ocultar o botão Manage App, rodapé e cabeçalho
    # hide_st_style = """
    # <style>
    # #MainMenu {visibility: hidden;} 
    # footer {visibility: hidden;} 
    # header {visibility: hidden;} 
    # .stDeployButton {visibility: hidden;}  /* Oculta o botão Deploy */
    # [data-testid="stStatusWidget"] {visibility: hidden;}  /* Oculta os botões de status */
    # </style>
    # """
    
    # # Aplicar o CSS
    # st.markdown(hide_st_style, unsafe_allow_html=True)

    # Aplica o estilo padrão
    apply_default_style()    

    # 1. Título
    st.title("Relatório de Estoque")
    
    try:
        # Inicializar o estado para os totalizadores se não existir
        if 'totals' not in st.session_state:
            st.session_state.totals = None

        # Carregar dados com indicador de progresso
        data_service = DataService()
        table_name = 'Produtos'
        campos = [
            "CodigoInterno",
            "CodigoExpedicao",
            "Nome",
            "Descricao",
            "NomeGrupo",
            'EstoqueGalpao',
            "ValorCusto",
            "ValorVenda",
            "Localizacao"
        ]        
        
        # Adicionar cache com TTL de 5 minutos
        @st.cache_data(ttl=300)
        def get_cached_data():
            return load_data(data_service, table_name, campos)
        
        df = get_cached_data()
        
        # Converter colunas numéricas
        df["EstoqueGalpao"] = pd.to_numeric(df['EstoqueGalpao'], errors='coerce')
        df['ValorCusto'] = pd.to_numeric(df['ValorCusto'], errors='coerce')
        df['ValorVenda'] = pd.to_numeric(df['ValorVenda'], errors='coerce')
        
        # Container para os totalizadores
        totals_container = st.container()
        
        # 3. Grid
        grid_options = create_grid_options(df)
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=800,
            fit_columns_on_grid_load=True,
            theme='alpine',
            allow_unsafe_jscode=True,
            reload_data=True,
            key='grid'
        )
        
        # Atualizar totalizadores
        st.session_state.totals = calculate_totals(grid_response['data'])
        
        # Exibir totalizadores no container do topo
        with totals_container:
            if st.session_state.totals:
                display_totals(st.session_state.totals, grid_response['data'])
        st.markdown("---")
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
