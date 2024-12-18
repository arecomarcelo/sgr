import streamlit as st
from service import DataService
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from io import BytesIO
import locale

# Tentar configurar a localidade
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    st.warning("A localidade 'pt_BR.UTF-8' não está disponível. Usando a localidade padrão.")
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
        if 'Estoque' in df.columns:
            df_formatted['Estoque'] = df_formatted['Estoque'].apply(
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
    estoque = pd.to_numeric(data['Estoque'], errors='coerce')
    valor_custo = pd.to_numeric(data['ValorCusto'], errors='coerce')
    valor_venda = pd.to_numeric(data['ValorVenda'], errors='coerce')
    
    return {
        'total_produtos': float(estoque.sum()),
        'total_custo': float(valor_custo.sum()),
        'total_venda': float(valor_venda.sum())
    }

def display_totals(totals):
    col1, col2, col3 = st.columns(3)
    
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

def create_grid_options(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_grid_options(
        domLayout='normal',
        enableRangeSelection=True,
        enableCellTextSelection=True,
        suppressRowClickSelection=True,
        enableExcelExport=True,
        enableCsvExport=True,
        quickFilterText='',
        onFirstDataRendered='onFirstDataRendered',
        onFilterChanged='onFilterChanged'
    )
    
    # Configurações de coluna
    gb.configure_default_column(
        filter=True,
        cellStyle={'border': '1px solid black'},
        floatingFilter=True
    )
    
    # Configurar colunas visíveis
    for column in df.columns:
        gb.configure_column(column, hide=False)
    
    # Configurações específicas para colunas numéricas
    gb.configure_column(
        "ValorCusto",
        type=["numericColumn", "numberColumnFilter"],
        valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFraction Digits: 2, maximumFractionDigits: 2})"
    )
    gb.configure_column(
        "ValorVenda",
        type=["numericColumn", "numberColumnFilter"],
        valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})"
    )
    gb.configure_column(
        "Estoque",
        type=["numericColumn", "numberColumnFilter"],
        valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 0})"
    )
    
    # Totalizadores
    gb.configure_column("Estoque", aggFunc="sum", header_name="Total Estoque")
    gb.configure_column("ValorCusto", aggFunc="sum", header_name="Total Custo")
    gb.configure_column("ValorVenda", aggFunc="sum", header_name="Total Venda")
    
    return gb.build()

def apply_global_filter(df, filter_text):
    if not filter_text:
        return df
    
    # Converter o texto do filtro para minúsculo para busca case-insensitive
    filter_text = filter_text.lower()
    
    # Aplicar filtro em todas as colunas
    mask = df.astype(str).apply(lambda x: x.str.lower()).apply(
        lambda x: x.str.contains(filter_text, na=False)
    ).any(axis=1)
    
    return df[mask]

def main():
    st.set_page_config(
        page_title="Relatório de Estoque",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 1. Título
    st.title("Relatório de Estoque")
    
    try:
        # Inicializar o estado para os totalizadores se não existir
        if 'totals' not in st.session_state:
            st.session_state.totals = None

        # Carregar dados com indicador de progresso
        data_service = DataService()
        table_name = '"Produtos"'
        campos = '"CodigoInterno" as "Código Gestão","CodigoExpedicao" as "Código Expedição", "Nome", "Descricao" as "Descrição",  "NomeGrupo" as "Grupo", "EstoqueGalpao" as "Estoque", "ValorCusto", "ValorVenda", "Localizacao" as "Localização"'
        
        # Adicionar cache com TTL de 5 minutos
        @st.cache_data(ttl=300)
        def get_cached_data():
            return load_data(data_service, table_name, campos)
        
        df = get_cached_data()
        
        # Converter colunas numéricas
        df['Estoque'] = pd.to_numeric(df['Estoque'], errors='coerce')
        df['ValorCusto'] = pd.to_numeric(df['ValorCusto'], errors='coerce')
        df['ValorVenda'] = pd.to_numeric(df['ValorVenda'], errors='coerce')
        
        # Container para os totalizadores
        totals_container = st.container()
        
        # Adicionar filtro global e botão de download
        col1, col2 = st.columns([3, 1])
        with col1:
            global_filter = st.text_input("🔍 Filtro Global", "")
        
        # Aplicar filtro global se necessário
        if global_filter:
            df = apply_global_filter(df, global_filter)
        
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
                display_totals(st.session_state.totals)
                st.markdown("---")
        
        # Botão de download (usando dados filtrados)
        with col2:
            if st.download_button(
                label="📥 Download Excel",
                data=download_excel(grid_response['data']),
                file_name="relatorio_estoque.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                st.success("Download iniciado!")
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()