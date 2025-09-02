"""
SGR - Módulo de Vendas
Compatível com o sistema principal de login e menu
"""
import logging
import os
import traceback
from datetime import date, datetime

import django
from django.conf import settings

import pandas as pd
import streamlit as st

# Django já configurado pelo app.py principal

# Imports da aplicação refatorada
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
except ImportError as e:
    st.error(f"❌ Erro crítico de importação: {e}")
    st.stop()


class VendasControllerIntegrado:
    """Controller de vendas integrado ao sistema principal"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.container = None
        self.vendas_service = None

        # Inicializar serviços
        self._initialize_services()

    def _initialize_services(self):
        """Inicializa serviços com tratamento de erro"""
        try:
            self.container = DIContainer()
            self.vendas_service = self.container.get_vendas_service()
            self.logger.info("Serviços de vendas inicializados com sucesso")

        except Exception as e:
            self.logger.error(f"Erro na inicialização: {str(e)}")
            st.error(f"❌ Erro na inicialização: {str(e)}")
            st.error("Verifique a configuração do banco de dados no arquivo .env")
            st.stop()

    def render_dashboard(self):
        """Renderiza dashboard principal de vendas"""
        try:
            # Aplicar tema
            apply_theme()

            # Header
            st.markdown(
                "<h1 style='text-align: center; color: #1E88E5;'>📊 Dashboard de Vendas</h1>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            # Verificar saúde do sistema
            if not self._health_check():
                return

            # Renderizar seções
            self._render_update_info()
            self._render_filters_and_data()
            self._render_analysis()

        except Exception as e:
            self.logger.error(f"Erro no dashboard: {str(e)}")
            st.error("❌ Erro inesperado no dashboard. Verifique os logs.")
            with st.expander("Detalhes do erro"):
                st.code(traceback.format_exc())

    def _health_check(self) -> bool:
        """Verifica saúde do sistema"""
        try:
            health = self.container.health_check()

            if all(health.values()):
                st.success("✅ Sistema funcionando normalmente")
                return True
            else:
                failed_services = [k for k, v in health.items() if not v]
                st.error(f"❌ Serviços com problemas: {', '.join(failed_services)}")
                return False

        except Exception as e:
            st.error(f"❌ Erro no health check: {str(e)}")
            return False

    def _render_update_info(self):
        """Renderiza informações de atualização"""
        try:
            with st.expander("🔄 Informações de Atualização", expanded=False):
                info = self.vendas_service.get_informacoes_atualizacao()

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    st.metric("Data", info.get("data", "N/A"))
                with col2:
                    st.metric("Hora", info.get("hora", "N/A"))
                with col3:
                    st.metric("Período", info.get("periodo", "N/A"))
                with col4:
                    st.metric("Inseridos", info.get("inseridos", 0))
                with col5:
                    st.metric("Atualizados", info.get("atualizados", 0))

        except Exception as e:
            self.logger.warning(
                f"Erro ao carregar informações de atualização: {str(e)}"
            )

    def _render_filters_and_data(self):
        """Renderiza filtros e dados"""
        st.subheader("🔍 Filtros e Dados")

        # Inicializar dados na sessão
        if "vendas_df" not in st.session_state:
            st.session_state.vendas_df = None
        if "vendas_metricas" not in st.session_state:
            st.session_state.vendas_metricas = None

        # Seção de filtros
        with st.expander("Configurar Filtros", expanded=True):
            self._render_filters()

        # Exibir dados e métricas
        if st.session_state.vendas_df is not None:
            self._render_metrics()
            self._render_data_table()

    def _render_filters(self):
        """Renderiza seção de filtros"""
        try:
            filter_form = FilterForm()

            # Carregar opções
            with st.spinner("Carregando opções..."):
                vendedores = self.vendas_service.get_vendedores_ativos()
                situacoes = self.vendas_service.get_situacoes_disponiveis()

            # Renderizar filtros
            filters = filter_form.render_filters(vendedores, situacoes)

            # Botões de ação
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔍 Aplicar Filtros", type="primary"):
                    self._apply_filters(filters)

            with col2:
                if st.button("📅 Dados do Mês Atual"):
                    self._load_current_month_data()

        except Exception as e:
            st.error(f"❌ Erro nos filtros: {str(e)}")

    def _apply_filters(self, filters: dict):
        """Aplica filtros e carrega dados"""
        try:
            # Validar filtros
            if not filters.get("data_inicio") or not filters.get("data_fim"):
                st.error("❌ Datas inicial e final são obrigatórias")
                return

            if not ValidationHelper.validate_date_range(
                filters["data_inicio"], filters["data_fim"]
            ):
                return

            # Carregar dados
            with st.spinner("Carregando dados de vendas..."):
                df_vendas = self.vendas_service.get_vendas_filtradas(
                    data_inicio=filters["data_inicio"],
                    data_fim=filters["data_fim"],
                    vendedores=filters["vendedores"] if filters["vendedores"] else None,
                    situacoes=filters["situacoes"] if filters["situacoes"] else None,
                )

            # Calcular métricas
            with st.spinner("Calculando métricas..."):
                metricas = self.vendas_service.get_metricas_vendas(df_vendas)

            # Armazenar na sessão
            st.session_state.vendas_df = df_vendas
            st.session_state.vendas_metricas = metricas

            if df_vendas.empty:
                st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados")
            else:
                st.success(f"✅ {len(df_vendas)} registros carregados com sucesso")
                st.rerun()

        except ValidationError as e:
            st.error(f"❌ Erro de validação: {str(e)}")
        except BusinessLogicError as e:
            st.error(f"❌ Erro de negócio: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro ao aplicar filtros: {str(e)}")
            self.logger.error(f"Erro ao aplicar filtros: {str(e)}")

    def _load_current_month_data(self):
        """Carrega dados do mês atual"""
        try:
            with st.spinner("Carregando dados do mês atual..."):
                df_vendas = self.vendas_service.get_vendas_mes_atual()
                metricas = self.vendas_service.get_metricas_vendas(df_vendas)

            st.session_state.vendas_df = df_vendas
            st.session_state.vendas_metricas = metricas

            st.success(f"✅ {len(df_vendas)} vendas do mês atual carregadas")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Erro ao carregar dados do mês atual: {str(e)}")

    def _render_metrics(self):
        """Renderiza métricas"""
        if st.session_state.vendas_metricas:
            st.subheader("📊 Resumo Executivo")
            metrics_display = MetricsDisplay()
            metrics_display.render_metrics_cards(st.session_state.vendas_metricas)
            st.markdown("---")

    def _render_data_table(self):
        """Renderiza tabela de dados"""
        df = st.session_state.vendas_df

        if df is None or df.empty:
            return

        st.subheader("📋 Dados Detalhados")

        # Preparar dados para exibição
        try:
            colunas_exibir = [
                "ClienteNome",
                "VendedorNome",
                "ValorProdutos",
                "ValorDesconto",
                "ValorTotal",
                "Data",
            ]
            df_display = df[colunas_exibir].copy()

            # Formatar valores monetários
            for col in ["ValorProdutos", "ValorDesconto", "ValorTotal"]:
                if col in df_display.columns:
                    df_display[col] = df_display[col].apply(
                        lambda x: f"R$ {float(x):,.2f}".replace(".", "#")
                        .replace(",", ".")
                        .replace("#", ",")
                        if pd.notna(x)
                        and str(x).replace(".", "").replace(",", "").isdigit()
                        else str(x)
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

            # Exibir grid
            data_grid = DataGrid()
            data_grid.render_data_grid(
                df_display,
                title=f"Vendas Detalhadas ({len(df_display)} registros)",
                show_download=True,
                filename_prefix="vendas_detalhadas",
            )

        except Exception as e:
            st.error(f"❌ Erro ao exibir tabela: {str(e)}")
            # Fallback: mostrar dataframe básico
            st.dataframe(df.head(100), use_container_width=True)

    def _render_analysis(self):
        """Renderiza análises avançadas"""
        df = st.session_state.vendas_df

        if df is None or df.empty:
            return

        with st.expander("📈 Análise Avançada", expanded=False):
            try:
                # Análise por vendedor
                vendas_por_vendedor = self.vendas_service.get_vendas_por_vendedor(
                    df, top_n=10
                )

                if not vendas_por_vendedor.empty:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("🏆 Top 10 Vendedores - Valor")
                        st.dataframe(
                            vendas_por_vendedor[
                                ["VendedorNome", "total_valor", "quantidade"]
                            ]
                        )

                    with col2:
                        st.subheader("📊 Resumo Estatístico")
                        if len(vendas_por_vendedor) > 0:
                            st.metric(
                                "Vendedor Mais Produtivo",
                                vendas_por_vendedor.iloc[0]["VendedorNome"],
                            )
                            valor_formatado = f"R$ {vendas_por_vendedor.iloc[0]['total_valor']:,.2f}".replace(
                                ",", "."
                            )
                            st.metric("Maior Valor", valor_formatado)

                # Tendência temporal
                if "Data" in df.columns:
                    tendencia = self.vendas_service.get_tendencia_vendas(df)

                    if not tendencia.empty:
                        st.subheader("📈 Tendência por Período")
                        st.dataframe(tendencia)

            except Exception as e:
                st.error(f"❌ Erro na análise: {str(e)}")


def main(key=None):
    """
    Função principal do módulo de vendas (compatível com app.py)

    Args:
        key: Chave única para o módulo (requerido pela aplicação principal)
    """
    try:
        # Criar e executar controller
        controller = VendasControllerIntegrado()
        controller.render_dashboard()

    except Exception as e:
        st.error("❌ Erro fatal no módulo de vendas")
        st.error(str(e))
        logging.error(f"Erro fatal no módulo de vendas: {str(e)}")


# Para execução direta (desenvolvimento)
if __name__ == "__main__":
    main()
