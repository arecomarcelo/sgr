"""
Componentes de formulário específicos para Vendas
Formulários simples e reutilizáveis para filtros de vendas
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

import streamlit as st


class FilterForm:
    """Formulário de filtros para vendas"""

    def __init__(self):
        self.key_prefix = "vendas_filter_"

    def render_filters(
        self, vendedores_disponiveis: List[str], situacoes_disponiveis: List[str]
    ) -> Dict[str, Any]:
        """
        Renderiza formulário de filtros para vendas

        Args:
            vendedores_disponiveis: Lista de vendedores disponíveis
            situacoes_disponiveis: Lista de situações disponíveis

        Returns:
            Dict com valores dos filtros
        """
        filters: Dict[str, Any] = {}

        # Filtros de data
        col1, col2 = st.columns(2)

        with col1:
            # Data inicial - padrão primeiro dia do mês atual
            hoje = datetime.now()
            data_inicial_default = datetime(hoje.year, hoje.month, 1).date()

            data_inicio_input = st.date_input(
                "📅 Data Inicial",
                value=data_inicial_default,
                max_value=datetime.now().date(),
                format="DD/MM/YYYY",
                key=f"{self.key_prefix}data_inicio",
                help="Selecione a data inicial do período",
            )
            # st.date_input pode retornar date ou tuple, garantir que é date
            if isinstance(data_inicio_input, date):
                filters["data_inicio"] = data_inicio_input
            else:
                filters["data_inicio"] = data_inicio_input[0]

        with col2:
            # Data final - padrão hoje
            data_fim_input = st.date_input(
                "📅 Data Final",
                value=datetime.now().date(),
                max_value=datetime.now().date(),
                format="DD/MM/YYYY",
                key=f"{self.key_prefix}data_fim",
                help="Selecione a data final do período",
            )
            # st.date_input pode retornar date ou tuple, garantir que é date
            if isinstance(data_fim_input, date):
                filters["data_fim"] = data_fim_input
            else:
                filters["data_fim"] = data_fim_input[0]

        # Filtros de vendedor e situação
        col3, col4 = st.columns(2)

        with col3:
            filters["vendedores"] = st.multiselect(
                "👤 Vendedores",
                options=vendedores_disponiveis,
                default=[],
                key=f"{self.key_prefix}vendedores",
                help="Selecione um ou mais vendedores (vazio = todos)",
            )

        with col4:
            filters["situacoes"] = st.multiselect(
                "📊 Situações",
                options=situacoes_disponiveis,
                default=[],
                key=f"{self.key_prefix}situacoes",
                help="Selecione uma ou mais situações (vazio = todas)",
            )

        # Validar datas
        if filters["data_inicio"] and filters["data_fim"]:
            if filters["data_inicio"] > filters["data_fim"]:
                st.error("❌ Data inicial não pode ser maior que data final")
                return {}

        return filters


class MetricsDisplay:
    """Componente para exibição de métricas"""

    def render_metrics_cards(self, metrics: Dict[str, Any]):
        """
        Renderiza cards de métricas

        Args:
            metrics: Dicionário com métricas calculadas
        """
        # Primeira linha: Total Entradas, Total Parcelado, Valor Total
        col1, col2, col3 = st.columns(3)

        with col1:
            entradas = metrics.get("total_entradas", 0)
            valor_formatado = self._format_currency(entradas)
            st.metric(
                label="💰 Total Entradas",
                value=valor_formatado,
                help="Valor total já recebido",
            )

        with col2:
            parcelado = metrics.get("total_parcelado", 0)
            parcelado_formatado = self._format_currency(parcelado)
            st.metric(
                label="⏳ Total Parcelado",
                value=parcelado_formatado,
                help="Valor total a receber",
            )

        with col3:
            total_valor = metrics.get("total_valor", 0)
            total_formatado = self._format_currency(total_valor)
            st.metric(
                label="💎 Valor Total",
                value=total_formatado,
                help="Valor total das vendas",
            )

        # Segunda linha: Total de Vendas, Ticket Médio, Margem Média
        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                label="📊 Total de Vendas",
                value=f"{metrics.get('total_quantidade', 0):,}".replace(",", "."),
                help="Quantidade total de vendas no período",
            )

        with col5:
            ticket_medio = metrics.get("ticket_medio", 0)
            ticket_formatado = self._format_currency(ticket_medio)
            st.metric(
                label="🎯 Ticket Médio",
                value=ticket_formatado,
                help="Valor médio por venda",
            )

        with col6:
            margem_media = metrics.get("margem_media", 0)
            if margem_media > 0:
                st.metric(
                    label="📈 Margem Média",
                    value=f"{margem_media:.2f}%",
                    help="Margem média das vendas",
                )
            else:
                st.metric(
                    label="📈 Margem Média",
                    value="N/A",
                    help="Dados de margem não disponíveis",
                )

    def _format_currency(self, value: float) -> str:
        """
        Formata valor como moeda brasileira

        Args:
            value: Valor numérico

        Returns:
            str: Valor formatado
        """
        return f"R$ {value:,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")


class ValidationHelper:
    """Helper para validações de formulários"""

    @staticmethod
    def validate_date_range(data_inicio: date, data_fim: date) -> bool:
        """
        Valida intervalo de datas

        Args:
            data_inicio: Data inicial
            data_fim: Data final

        Returns:
            bool: True se válido
        """
        if not data_inicio or not data_fim:
            st.error("❌ Datas inicial e final são obrigatórias")
            return False

        if data_inicio > data_fim:
            st.error("❌ Data inicial não pode ser maior que data final")
            return False

        # Verificar se o intervalo não é muito grande
        diff_days = (data_fim - data_inicio).days
        if diff_days > 365:
            st.warning("⚠️ Período muito longo pode afetar a performance")

        return True

    @staticmethod
    def show_error(message: str):
        """Exibe mensagem de erro"""
        st.error(f"❌ {message}")

    @staticmethod
    def show_warning(message: str):
        """Exibe mensagem de aviso"""
        st.warning(f"⚠️ {message}")

    @staticmethod
    def show_success(message: str):
        """Exibe mensagem de sucesso"""
        st.success(f"✅ {message}")

    @staticmethod
    def show_info(message: str):
        """Exibe mensagem informativa"""
        st.info(f"ℹ️ {message}")


class LoadingHelper:
    """Helper para estados de loading"""

    @staticmethod
    def show_loading(message: str = "Carregando..."):
        """Exibe estado de loading"""
        return st.empty().info(f"⏳ {message}")

    @staticmethod
    def hide_loading(loading_element):
        """Remove estado de loading"""
        if loading_element:
            loading_element.empty()

    @staticmethod
    def with_loading(func, message: str = "Processando..."):
        """
        Executa função com loading

        Args:
            func: Função a ser executada
            message: Mensagem de loading

        Returns:
            Resultado da função
        """
        loading = LoadingHelper.show_loading(message)
        try:
            result = func()
            LoadingHelper.hide_loading(loading)
            return result
        except Exception as e:
            LoadingHelper.hide_loading(loading)
            raise e
