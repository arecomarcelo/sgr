# # import streamlit as st
# # from service import DataService
# # from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
# # import pandas as pd
# # import base64
# # from io import BytesIO

# # @st.cache_data
# # def load_data(_service, table_name, fields):
# #     return _service.get_data(table_name, fields)

# # def download_link(data, filename, filetype):
# #     """Gera um link de download para o arquivo."""
# #     b64 = base64.b64encode(data).decode()  # Codifica os dados em base64
# #     return f'<a href="data:file/{filetype};base64,{b64}" download="{filename}">Download {filename}</a>'

# # def export_to_csv(df):
# #     """Exporta o DataFrame para CSV."""
# #     csv = df.to_csv(index=False)
# #     return download_link(csv.encode(), 'data.csv', 'csv')

# # def export_to_excel(df):
# #     """Exporta o DataFrame para Excel."""
# #     output = BytesIO()
# #     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
# #         df.to_excel(writer, index=False, sheet_name='Sheet1')
# #     return download_link(output.getvalue(), 'data.xlsx', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# # def main():
# #     st.set_page_config(page_title="Relatório de Estoque", layout="wide")
# #     st.title("Relatório de Estoque")

# #     # Inicializar o serviço de dados sem parâmetros
# #     data_service = DataService()

# #     # Carregar dados de uma tabela com cache
# #     table_name = '"Produtos"'
# #     campos = '"CodigoInterno", "Nome", "Descricao", "NomeGrupo", "Estoque", "EstoqueGalpao", "ValorCusto", "ValorVenda", "Localizacao"'
# #     df = load_data(data_service, table_name, campos)

# #     # Criar opções de grid
# #     gb = GridOptionsBuilder.from_dataframe(df)
# #     gb.configure_grid_options(domLayout='normal')  # Garante barras de rolagem

# #     # Habilitar filtros para todas as colunas
# #     gb.configure_default_column(filter=True)  # Habilita filtro para todas as colunas
# #     gb.configure_default_column(
# #         cellStyle={'border': '1px solid black'}  # Adiciona borda a todas as células
# #     )

# #     # Habilitar o menu de colunas para permitir que os usuários ocultem/mostrem colunas
# #     for column in df.columns:
# #         gb.configure_column(column, hide=False)

# #     # Adicionar opções de exportação
# #     gb.configure_grid_options(
# #         enableRangeSelection=True,
# #         enableCellTextSelection=True,
# #         suppressRowClickSelection=True,
# #         onGridReady=JsCode("""
# #             function() {
# #                 var gridOptions = this.gridOptions;
# #                 var exportButton = document.createElement('button');
# #                 exportButton.innerHTML = 'Exportar para Excel';
# #                 exportButton.onclick = function() {
# #                     gridOptions.api.exportDataAsExcel();
# #                 };
# #                 this.eGridDiv.appendChild(exportButton);
# #             }
# #         """)
# #     )

# #     grid_options = gb.build()

# #     # Renderizar a grid
# #     AgGrid(df,
# #            gridOptions=grid_options,
# #            height=800,
# #            fit_columns_on_grid_load=True,
# #            theme='alpine')  # Define o tema

# # if __name__ == "__main__":
# #     main()

# import streamlit as st
# from service import DataService
# from st_aggrid import AgGrid, GridOptionsBuilder
# import pandas as pd

# @st.cache_data
# def load_data(_service, table_name, fields):
#     return _service.get_data(table_name, fields)

# def main():
#     st.set_page_config(page_title="Relatório de Estoque", layout="wide")
#     st.title("Relatório de Estoque")

#     # Inicializar o serviço de dados sem parâmetros
#     data_service = DataService()

#     # Carregar dados de uma tabela com cache
#     table_name = '"Produtos"'
#     campos = '"CodigoInterno", "Nome", "Descricao", "NomeGrupo", "Estoque", "EstoqueGalpao", "ValorCusto", "ValorVenda", "Localizacao"'
#     df = load_data(data_service, table_name, campos)

#     # Criar opções de grid
#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_grid_options(domLayout='normal')  # Garante barras de rolagem

#     # Habilitar filtros para todas as colunas
#     gb.configure_default_column(filter=True)  # Habilita filtro para todas as colunas
#     gb.configure_default_column(
#         cellStyle={'border': '1px solid black'}  # Adiciona borda a todas as células
#     )

#     # Habilitar o menu de colunas para permitir que os usuários ocultem/mostrem colunas
#     for column in df.columns:
#         gb.configure_column(column, hide=False)

#     # Adicionar opções de exportação
#     gb.configure_grid_options(
#         enableRangeSelection=True,
#         enableCellTextSelection=True,
#         suppressRowClickSelection=True,
#         enableExcelExport=True,  # Habilita a exportação para Excel
#         enableCsvExport=True  # Habilita a exportação para CSV
#     )

#     grid_options = gb.build()

#     # Renderizar a grid
#     grid_response = AgGrid(df,
#                            gridOptions=grid_options,
#                            height=800,
#                            fit_columns_on_grid_load=True,
#                            theme='alpine',
#                            allow_unsafe_jscode=True)  # Permite execução de JS

# if __name__ == "__main__":
#     main()

import streamlit as st
from service import DataService
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

@st.cache_data
def load_data(_service, table_name, fields):
    return _service.get_data(table_name, fields)

def format_currency(value):
    """Formata o valor para o formato desejado (ex: 399.00 -> 399,00)."""
    try:
        # Converte o valor para float e formata
        return f"{float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return value  # Retorna o valor original se não puder ser convertido

def main():
    st.set_page_config(page_title="Relatório de Estoque", layout="wide")
    st.title("Relatório de Estoque")

    # Inicializar o serviço de dados sem parâmetros
    data_service = DataService()

    # Carregar dados de uma tabela com cache
    table_name = '"Produtos"'
    # campos = '"CodigoInterno", "Nome", "Descricao", "NomeGrupo", "EstoqueGalpao" as Estoque, "ValorCusto", "ValorVenda", "Localizacao"'
    campos = '"CodigoInterno" as "Código Gestão","CodigoExpedicao" as "Código Expedição", "Nome", "Descricao" as "Descrição",  "NomeGrupo" as "Grupo", "EstoqueGalpao" as "Estoque", "ValorCusto", "ValorVenda", "Localizacao" as "Localização"'
    df = load_data(data_service, table_name, campos)

    # Garantir que as colunas de valor sejam numéricas
    df['ValorCusto'] = pd.to_numeric(df['ValorCusto'], errors='coerce')
    df['ValorVenda'] = pd.to_numeric(df['ValorVenda'], errors='coerce')

    # Formatar as colunas de valor
    df['ValorCusto'] = df['ValorCusto'].apply(format_currency)
    df['ValorVenda'] = df['ValorVenda'].apply(format_currency)

    # Criar opções de grid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_grid_options(domLayout='normal')  # Garante barras de rolagem

    # Habilitar filtros para todas as colunas
    gb.configure_default_column(filter=True)  # Habilita filtro para todas as colunas
    gb.configure_default_column(
        cellStyle={'border': '1px solid black'}  # Adiciona borda a todas as células
    )

    # Habilitar o menu de colunas para permitir que os usuários ocultem/mostrem colunas
    for column in df.columns:
        gb.configure_column(column, hide=False)

    # Adicionar opções de exportação
    gb.configure_grid_options(
        enableRangeSelection=True,
        enableCellTextSelection=True,
        suppressRowClickSelection=True,
        enableExcelExport=True,  # Habilita a exportação para Excel
        enableCsvExport=True  # Habilita a exportação para CSV
    )

    grid_options = gb.build()

    # Renderizar a grid
    grid_response = AgGrid(df,
                           gridOptions=grid_options,
                           height=800,
                           fit_columns_on_grid_load=True,
                           theme='alpine',
                           allow_unsafe_jscode=True)  # Permite execução de JS

if __name__ == "__main__":
    main()