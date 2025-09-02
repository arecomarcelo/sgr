"""
Componentes reutilizáveis de grade de dados para SGR
Implementa padrão Component para elementos de UI
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridOptionsBuilder, GridUpdateMode

from core.error_handler import handle_errors


class SelectionMode(Enum):
    """Modos de seleção da grade"""

    SINGLE = "single"
    MULTIPLE = "multiple"
    DISABLED = "disabled"


class GridTheme(Enum):
    """Temas disponíveis para a grade"""

    STREAMLIT = "streamlit"
    ALPINE = "alpine"
    BALHAM = "balham"
    MATERIAL = "material"


class GridComponentInterface(ABC):
    """Interface base para componentes de grade"""

    @abstractmethod
    def render(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Renderiza a grade

        Args:
            data: DataFrame com os dados

        Returns:
            Resultado da renderização da grade
        """
        pass


class StandardDataGrid(GridComponentInterface):
    """
    Componente de grade de dados padrão
    Configurável e reutilizável
    """

    def __init__(
        self,
        height: int = 400,
        selection_mode: SelectionMode = SelectionMode.SINGLE,
        theme: GridTheme = GridTheme.STREAMLIT,
        enable_enterprise_modules: bool = False,
        fit_columns_on_grid_load: bool = True,
        enable_sidebar: bool = False,
        update_mode: GridUpdateMode = GridUpdateMode.SELECTION_CHANGED,
    ):
        self.height = height
        self.selection_mode = selection_mode
        self.theme = theme
        self.enable_enterprise_modules = enable_enterprise_modules
        self.fit_columns_on_grid_load = fit_columns_on_grid_load
        self.enable_sidebar = enable_sidebar
        self.update_mode = update_mode

        # Configurações de coluna personalizadas
        self._column_configs: Dict[str, Dict[str, Any]] = {}

        # Callbacks personalizados
        self._on_selection_changed: Optional[Callable] = None

    def configure_column(
        self,
        field: str,
        header_name: str = None,
        width: int = None,
        min_width: int = None,
        max_width: int = None,
        resizable: bool = True,
        sortable: bool = True,
        filterable: bool = True,
        pinned: str = None,
        hide: bool = False,
        cell_renderer: str = None,
        value_formatter: str = None,
        **kwargs,
    ):
        """
        Configura uma coluna específica

        Args:
            field: Nome do campo
            header_name: Nome do cabeçalho
            width: Largura da coluna
            min_width: Largura mínima
            max_width: Largura máxima
            resizable: Se a coluna é redimensionável
            sortable: Se a coluna é ordenável
            filterable: Se a coluna é filtrável
            pinned: Posição do pin ('left', 'right')
            hide: Se a coluna deve estar oculta
            cell_renderer: Renderizador de célula personalizado
            value_formatter: Formatador de valor
            **kwargs: Outras configurações AG-Grid
        """
        config = {
            "field": field,
            "resizable": resizable,
            "sortable": sortable,
            "filter": filterable,
        }

        if header_name:
            config["headerName"] = header_name
        if width:
            config["width"] = width
        if min_width:
            config["minWidth"] = min_width
        if max_width:
            config["maxWidth"] = max_width
        if pinned:
            config["pinned"] = pinned
        if hide:
            config["hide"] = hide
        if cell_renderer:
            config["cellRenderer"] = cell_renderer
        if value_formatter:
            config["valueFormatter"] = value_formatter

        # Adicionar configurações extras
        config.update(kwargs)

        self._column_configs[field] = config
        return self

    def set_selection_callback(self, callback: Callable[[List[Dict]], None]):
        """
        Define callback para mudança de seleção

        Args:
            callback: Função a ser chamada quando seleção muda
        """
        self._on_selection_changed = callback
        return self

    @handle_errors(show_details=False)
    def render(self, data: pd.DataFrame, key: str = None) -> Dict[str, Any]:
        """
        Renderiza a grade de dados

        Args:
            data: DataFrame com os dados
            key: Chave única do componente

        Returns:
            Resultado da grade com dados selecionados
        """
        if data.empty:
            st.warning("📭 Nenhum dado encontrado para exibir")
            return {"selected_rows": [], "data": data}

        # Configurar opções da grade
        gb = self._build_grid_options(data)

        # Renderizar grade
        grid_response = AgGrid(
            data,
            gridOptions=gb.build(),
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            update_mode=self.update_mode,
            height=self.height,
            fit_columns_on_grid_load=self.fit_columns_on_grid_load,
            theme=self.theme.value,
            enable_enterprise_modules=self.enable_enterprise_modules,
            allow_unsafe_jscode=True,
            key=key,
        )

        # Processar callback de seleção se definido
        if self._on_selection_changed and "selected_rows" in grid_response:
            try:
                selected_data = grid_response["selected_rows"]
                if isinstance(selected_data, pd.DataFrame):
                    selected_data = selected_data.to_dict("records")
                self._on_selection_changed(selected_data)
            except Exception as e:
                st.error(f"Erro no callback de seleção: {str(e)}")

        return grid_response

    def _build_grid_options(self, data: pd.DataFrame) -> GridOptionsBuilder:
        """Constrói as opções da grade"""
        gb = GridOptionsBuilder.from_dataframe(data)

        # Configurações gerais
        gb.configure_grid_options(
            domLayout="normal",
            enableRangeSelection=True,
            enableCellTextSelection=True,
            suppressRowClickSelection=(self.selection_mode == SelectionMode.DISABLED),
            enableExcelExport=True,
            enableCsvExport=True,
            sideBar=self.enable_sidebar,
        )

        # Configuração de seleção
        if self.selection_mode != SelectionMode.DISABLED:
            gb.configure_selection(
                selection_mode=self.selection_mode.value,
                use_checkbox=True
                if self.selection_mode == SelectionMode.MULTIPLE
                else False,
            )

        # Configurações padrão de coluna
        gb.configure_default_column(
            filter=True,
            sortable=True,
            resizable=True,
            cellStyle={"fontSize": "14px", "fontFamily": "Arial, sans-serif"},
        )

        # Aplicar configurações de colunas específicas
        for field, config in self._column_configs.items():
            if field in data.columns:
                gb.configure_column(field, **config)

        return gb


class ReportDataGrid(StandardDataGrid):
    """
    Grade especializada para relatórios
    Com configurações otimizadas para exibição de dados
    """

    def __init__(self, **kwargs):
        # Configurações padrão para relatórios
        defaults = {
            "height": 500,
            "selection_mode": SelectionMode.MULTIPLE,
            "enable_sidebar": True,
            "fit_columns_on_grid_load": True,
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

        # Configurações específicas para relatórios
        self._setup_report_defaults()

    def _setup_report_defaults(self):
        """Configura padrões para relatórios"""
        # Configurações comuns para campos de valor
        money_config = {
            "cellStyle": {"textAlign": "right"},
            "valueFormatter": "params.value?.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})",
        }

        # Configurações para números
        number_config = {
            "cellStyle": {"textAlign": "right"},
            "valueFormatter": "params.value?.toLocaleString('pt-BR')",
        }

        # Configurações para datas
        date_config = {
            "cellStyle": {"textAlign": "center"},
            "valueFormatter": "params.value ? new Date(params.value).toLocaleDateString('pt-BR') : ''",
        }

        # Aplicar configurações por padrões de nome
        self._default_formatters = {
            "valor": money_config,
            "custo": money_config,
            "venda": money_config,
            "preco": money_config,
            "quantidade": number_config,
            "estoque": number_config,
            "data": date_config,
            "vencimento": date_config,
            "envio": date_config,
        }

    def render(self, data: pd.DataFrame, key: str = None) -> Dict[str, Any]:
        """
        Renderiza grade com formatação automática

        Args:
            data: DataFrame com dados
            key: Chave única

        Returns:
            Resultado da grade
        """
        # Aplicar formatação automática baseada em nomes de colunas
        self._auto_configure_columns(data)

        return super().render(data, key)

    def _auto_configure_columns(self, data: pd.DataFrame):
        """Aplica configuração automática baseada nos nomes das colunas"""
        for column in data.columns:
            column_lower = column.lower()

            # Procurar por padrões conhecidos
            for pattern, config in self._default_formatters.items():
                if pattern in column_lower:
                    if column not in self._column_configs:
                        self.configure_column(column, **config)
                    break


class FilterableDataGrid(StandardDataGrid):
    """
    Grade com filtros avançados
    Permite filtros personalizados na interface
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filters: Dict[str, Any] = {}

    def add_filter_widget(
        self,
        column: str,
        filter_type: str = "text",
        options: List[str] = None,
        default_value: Any = None,
    ):
        """
        Adiciona widget de filtro para uma coluna

        Args:
            column: Nome da coluna
            filter_type: Tipo do filtro ('text', 'select', 'number', 'date')
            options: Opções para filtro select
            default_value: Valor padrão
        """
        self._filters[column] = {
            "type": filter_type,
            "options": options,
            "default": default_value,
            "value": None,
        }
        return self

    def render_filters(self, data: pd.DataFrame):
        """Renderiza os widgets de filtro"""
        if not self._filters:
            return data

        filtered_data = data.copy()

        # Criar colunas para os filtros
        filter_cols = st.columns(len(self._filters))

        for idx, (column, filter_config) in enumerate(self._filters.items()):
            with filter_cols[idx]:
                filter_value = self._render_single_filter(column, filter_config, data)
                self._filters[column]["value"] = filter_value

                # Aplicar filtro se há valor
                if filter_value and column in filtered_data.columns:
                    filtered_data = self._apply_filter(
                        filtered_data, column, filter_value, filter_config["type"]
                    )

        return filtered_data

    def _render_single_filter(
        self, column: str, config: Dict[str, Any], data: pd.DataFrame
    ):
        """Renderiza um widget de filtro específico"""
        filter_type = config["type"]

        if filter_type == "select":
            options = config["options"] or [""] + sorted(
                data[column].dropna().unique().tolist()
            )
            return st.selectbox(f"Filtrar {column}", options, key=f"filter_{column}")

        elif filter_type == "text":
            return st.text_input(f"Filtrar {column}", key=f"filter_{column}")

        elif filter_type == "number":
            return st.number_input(f"Filtrar {column}", key=f"filter_{column}")

        elif filter_type == "date":
            return st.date_input(f"Filtrar {column}", key=f"filter_{column}")

        return None

    def _apply_filter(
        self, data: pd.DataFrame, column: str, value: Any, filter_type: str
    ) -> pd.DataFrame:
        """Aplica filtro aos dados"""
        if filter_type == "select" and value:
            return data[data[column] == value]

        elif filter_type == "text" and value:
            return data[
                data[column].astype(str).str.contains(value, case=False, na=False)
            ]

        elif filter_type == "number" and value is not None:
            return data[data[column] == value]

        elif filter_type == "date" and value:
            return data[data[column] == value]

        return data

    def render(self, data: pd.DataFrame, key: str = None) -> Dict[str, Any]:
        """Renderiza grade com filtros"""
        if self._filters:
            filtered_data = self.render_filters(data)
            return super().render(filtered_data, key)

        return super().render(data, key)
