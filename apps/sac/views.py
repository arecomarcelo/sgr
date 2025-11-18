"""
SGR - Módulo SAC - Ordem de Serviço
Dashboard para visualização e gestão de Ordens de Serviço
"""

import io
import logging
from datetime import datetime

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from infrastructure.database.repositories_sac import SacAtualizacaoRepository

logger = logging.getLogger(__name__)


class OSController:
    """Controller para gerenciamento de Ordens de Serviço"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.atualizacao_repository = SacAtualizacaoRepository()

    def render_dashboard(self):
        """Renderiza dashboard principal de OS"""
        try:
            # Header
            st.markdown(
                "<h1 style='text-align: center; color: #1E88E5;'>🛠️ SAC - Ordens de Serviço</h1>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            # Inicializar dados na sessão
            if "os_df" not in st.session_state:
                st.session_state.os_df = None
            if "os_df_total" not in st.session_state:
                st.session_state.os_df_total = None
            if "os_selected_ids" not in st.session_state:
                st.session_state.os_selected_ids = None

            # Carregar dados do mês atual automaticamente na primeira vez
            if "os_auto_loaded" not in st.session_state:
                st.session_state.os_auto_loaded = True
                self._load_current_month_data(show_message=False)

            # Renderizar seções
            self._render_update_info()
            self._render_filters()
            self._render_metrics()
            self._render_data_table()
            self._render_products_table()

        except Exception as e:
            self.logger.error(f"Erro no dashboard de OS: {str(e)}")
            st.error(f"❌ Erro ao carregar dashboard: {str(e)}")

    def _render_update_info(self):
        """Renderiza informações de atualização do RPA de SAC"""
        try:
            with st.expander("🔄 Informações de Atualização", expanded=True):
                info = self._get_informacoes_atualizacao()

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Data", info.get("data", "N/A"))
                with col2:
                    st.metric("Hora", info.get("hora", "N/A"))
                with col3:
                    st.metric("Período", info.get("periodo", "N/A"))
                with col4:
                    st.metric("Inseridos", info.get("inseridos", 0))

        except Exception as e:
            self.logger.warning(
                f"Erro ao carregar informações de atualização: {str(e)}"
            )

    def _get_informacoes_atualizacao(self):
        """Obtém informações da última atualização do RPA de SAC"""
        try:
            df = self.atualizacao_repository.get_ultima_atualizacao()

            if df.empty:
                return {
                    "data": "N/A",
                    "hora": "N/A",
                    "periodo": "N/A",
                    "inseridos": 0,
                    "atualizados": 0,
                }

            registro = df.iloc[0]
            return {
                "data": registro.get("Data", "N/A"),
                "hora": registro.get("Hora", "N/A"),
                "periodo": registro.get("Periodo", "N/A"),
                "inseridos": registro.get("Inseridos", 0),
                "atualizados": registro.get("Atualizados", 0),
            }

        except Exception as e:
            self.logger.error(f"Erro ao obter informações de atualização: {str(e)}")
            return {
                "data": "N/A",
                "hora": "N/A",
                "periodo": "N/A",
                "inseridos": 0,
                "atualizados": 0,
            }

    def _render_filters(self):
        """Renderiza seção de filtros"""
        st.subheader("🔍 Filtros")

        with st.expander("Configurar Filtros", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                data_inicio = st.date_input(
                    "Data Início",
                    value=None,
                    help="Data inicial para filtro",
                    format="DD/MM/YYYY",
                )

            with col2:
                data_fim = st.date_input(
                    "Data Fim",
                    value=None,
                    help="Data final para filtro",
                    format="DD/MM/YYYY",
                )

            with col3:
                situacao_opcoes = self._get_situacoes_disponiveis()
                situacao_selecionada = st.multiselect(
                    "Situação",
                    options=situacao_opcoes,
                    help="Filtrar por situação da OS",
                )

            # Botões de ação
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔍 Aplicar Filtros", type="primary"):
                    self._apply_filters(data_inicio, data_fim, situacao_selecionada)

            with col2:
                if st.button("📋 Todas as OS"):
                    self._load_all_os()

    def _get_situacoes_disponiveis(self):
        """Retorna lista de situações disponíveis"""
        try:
            from core.models.modelos import OS

            situacoes = (
                OS.objects.values_list("SituacaoNome", flat=True)
                .distinct()
                .order_by("SituacaoNome")
            )
            return list(situacoes)
        except Exception as e:
            self.logger.error(f"Erro ao carregar situações: {str(e)}")
            return []

    def _apply_filters(self, data_inicio, data_fim, situacoes):
        """Aplica filtros e carrega dados"""
        try:
            from core.models.modelos import OS

            # Construir query para dados filtrados
            queryset = OS.objects.all()

            # Log dos filtros aplicados
            filtros_info = []

            if data_inicio:
                queryset = queryset.filter(Data__gte=data_inicio)
                filtros_info.append(f"Data >= {data_inicio.strftime('%d/%m/%Y')}")

            if data_fim:
                queryset = queryset.filter(Data__lte=data_fim)
                filtros_info.append(f"Data <= {data_fim.strftime('%d/%m/%Y')}")

            if situacoes:
                queryset = queryset.filter(SituacaoNome__in=situacoes)
                filtros_info.append(f"Situação: {', '.join(situacoes)}")

            # Converter para DataFrame
            df = self._queryset_to_dataframe(queryset)

            # Carregar dados totais (sem filtro) para métricas
            queryset_total = OS.objects.all()
            df_total = self._queryset_to_dataframe(queryset_total)

            # Limpar TODOS os dados antigos para forçar atualização
            st.session_state.os_df = df.copy()
            st.session_state.os_df_total = df_total.copy()
            st.session_state.os_selected_ids = None  # Limpar seleção anterior

            # Forçar limpeza de cache da grid
            if 'os_grid_key' in st.session_state:
                del st.session_state['os_grid_key']

            if df.empty:
                st.warning("⚠️ Nenhuma OS encontrada para os filtros selecionados")
            else:
                st.success(f"✅ {len(df)} OS encontradas")

        except Exception as e:
            st.error(f"❌ Erro ao aplicar filtros: {str(e)}")
            self.logger.error(f"Erro ao aplicar filtros: {str(e)}")
            import traceback

            self.logger.error(traceback.format_exc())

    def _load_all_os(self):
        """Carrega todas as OS"""
        try:
            from core.models.modelos import OS

            with st.spinner("Carregando todas as OS..."):
                queryset = OS.objects.all()
                df = self._queryset_to_dataframe(queryset)

                # Dados totais são os mesmos quando carrega tudo
                st.session_state.os_df = df.copy()
                st.session_state.os_df_total = df.copy()
                st.session_state.os_selected_ids = None

                # Limpar cache da grid
                if 'os_grid_key' in st.session_state:
                    del st.session_state['os_grid_key']

                st.success(f"✅ {len(df)} OS carregadas")
                # NÃO usar rerun - deixar renderizar naturalmente

        except Exception as e:
            st.error(f"❌ Erro ao carregar OS: {str(e)}")
            self.logger.error(f"Erro ao carregar OS: {str(e)}")

    def _load_current_month_data(self, show_message=True):
        """Carrega dados do mês atual (dia 1 até hoje)"""
        try:
            from datetime import date

            from core.models.modelos import OS

            # Calcular primeiro dia do mês atual e dia atual
            hoje = date.today()
            primeiro_dia = date(hoje.year, hoje.month, 1)

            with st.spinner("Carregando OS do mês atual..."):
                queryset = OS.objects.filter(Data__gte=primeiro_dia, Data__lte=hoje)
                df = self._queryset_to_dataframe(queryset)

                # Carregar dados totais (sem filtro) para métricas
                queryset_total = OS.objects.all()
                df_total = self._queryset_to_dataframe(queryset_total)

                st.session_state.os_df = df
                st.session_state.os_df_total = df_total

                if show_message and not df.empty:
                    st.success(
                        f"✅ {len(df)} OS do mês atual carregadas ({primeiro_dia.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')})"
                    )

        except Exception as e:
            st.error(f"❌ Erro ao carregar dados do mês atual: {str(e)}")
            self.logger.error(f"Erro ao carregar mês atual: {str(e)}")

    def _queryset_to_dataframe(self, queryset):
        """Converte queryset para DataFrame"""
        try:
            data = list(
                queryset.values(
                    "id",
                    "ID_Gestao",
                    "Data",
                    "ClienteNome",
                    "SituacaoNome",
                )
            )

            if not data:
                return pd.DataFrame()

            df = pd.DataFrame(data)

            # Formatar data
            if "Data" in df.columns:
                df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")

            return df

        except Exception as e:
            self.logger.error(f"Erro ao converter queryset: {str(e)}")
            return pd.DataFrame()

    def _render_metrics(self):
        """Renderiza métricas resumidas - sempre com dados totais"""
        df_total = st.session_state.os_df_total

        if df_total is None or df_total.empty:
            return

        st.markdown("---")
        st.subheader("📊 Resumo")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total de OS", len(df_total))

        with col2:
            if "SituacaoNome" in df_total.columns:
                situacoes_unicas = df_total["SituacaoNome"].nunique()
                st.metric("Situações Diferentes", situacoes_unicas)

        with col3:
            if "ClienteNome" in df_total.columns:
                clientes_unicos = df_total["ClienteNome"].nunique()
                st.metric("Clientes Únicos", clientes_unicos)

        with col4:
            if "Data" in df_total.columns:
                # Calcular período
                try:
                    datas = pd.to_datetime(df_total["Data"], format="%d/%m/%Y")
                    periodo_dias = (datas.max() - datas.min()).days
                    st.metric("Período (dias)", periodo_dias)
                except:
                    st.metric("Período", "N/A")

        st.markdown("---")

    def _render_data_table(self):
        """Renderiza tabela de dados usando AgGrid"""
        df = st.session_state.os_df

        if df is None or df.empty:
            st.info(
                "ℹ️ **Nenhum dado carregado ainda.**\n\n"
                "👆 Use os botões acima para:\n"
                "- **🔍 Aplicar Filtros**: Carregar dados com período e filtros personalizados\n"
                "- **📋 Todas as OS**: Carregar todas as Ordens de Serviço"
            )
            return

        st.subheader("📋 Ordens de Serviço")

        # Exibir informações sobre período de dados
        if "Data" in df.columns and not df.empty:
            try:
                # Converter datas para verificação
                datas_parsed = pd.to_datetime(
                    df["Data"], format="%d/%m/%Y", errors="coerce"
                )
                datas_validas = datas_parsed.dropna()

                if not datas_validas.empty:
                    data_min = datas_validas.min().strftime("%d/%m/%Y")
                    data_max = datas_validas.max().strftime("%d/%m/%Y")

                    st.info(
                        f"📅 **Período dos dados exibidos:** {data_min} a {data_max}"
                    )
            except Exception as e:
                self.logger.warning(f"Erro ao calcular período: {str(e)}")

        try:
            # Preparar dados para exibição
            df_display = df.copy()

            # Renomear colunas para exibição (INVERTIDO)
            column_mapping = {
                "id": "OS Código",
                "ID_Gestao": "ID_OS",
                "Data": "Data",
                "ClienteNome": "Cliente",
                "SituacaoNome": "Situação",
            }

            # Selecionar apenas as colunas que existem
            colunas_disponiveis = [
                col for col in column_mapping.keys() if col in df_display.columns
            ]
            df_display = df_display[colunas_disponiveis]
            df_display = df_display.rename(columns=column_mapping)

            # Mostrar informações do dataset
            st.metric("Total de Registros", len(df_display))

            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_display)

            gb.configure_grid_options(
                domLayout="normal",
                enableRangeSelection=True,
                enableCellTextSelection=True,
                suppressRowClickSelection=True,
            )

            # Configurações de coluna padrão
            gb.configure_default_column(
                filter=True,
                cellStyle={"border": "1px solid black"},
                floatingFilter=True,
                sortable=True,
            )

            # Configuração personalizada por coluna
            for col in df_display.columns:
                if col == "OS Código":
                    gb.configure_column(col, headerName="OS Código", width=120)
                elif col == "ID_OS":
                    gb.configure_column(col, headerName="ID_OS", width=150, hide=True)
                elif col == "Data":
                    gb.configure_column(
                        col,
                        headerName="Data",
                        type=["dateColumnFilter"],
                        width=120,
                    )
                elif col == "Cliente":
                    gb.configure_column(col, headerName="Cliente", width=250)
                elif col == "Situação":
                    gb.configure_column(col, headerName="Situação", width=150)

            grid_options = gb.build()

            # Gerar chave única baseada nos dados para forçar atualização
            import hashlib

            grid_key = hashlib.md5(
                str(df_display.values.tolist()).encode()
            ).hexdigest()[:8]

            # Renderizar AgGrid com chave dinâmica
            grid_response = AgGrid(
                df_display,
                gridOptions=grid_options,
                height=400,
                fit_columns_on_grid_load=True,
                theme="alpine",
                update_mode="MODEL_CHANGED",
                key=f"os_grid_{grid_key}",
            )

            # Capturar IDs das OS filtradas na grid (usa "OS Código" que contém o id/PK)
            if grid_response and "data" in grid_response:
                filtered_df = pd.DataFrame(grid_response["data"])
                if not filtered_df.empty and "OS Código" in filtered_df.columns:
                    st.session_state.os_selected_ids = filtered_df["OS Código"].tolist()
                else:
                    # Se não houver filtro aplicado, usar todos os IDs
                    if "id" in df.columns:
                        st.session_state.os_selected_ids = df["id"].tolist()

            # Seção de download
            st.markdown("---")
            st.subheader("📥 Download dos Dados")
            col1, col2 = st.columns(2)

            with col1:
                # Download CSV
                csv_data = df_display.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"os_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col2:
                # Download Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df_display.to_excel(writer, index=False, sheet_name="OS")

                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"os_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True,
                )

        except ImportError:
            st.error(
                "❌ AgGrid não está instalado. Instale com: pip install streamlit-aggrid"
            )
            # Fallback: mostrar dataframe básico
            st.dataframe(df_display, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erro ao exibir tabela: {str(e)}")
            self.logger.error(f"Erro ao renderizar grid: {str(e)}")
            # Fallback: mostrar dataframe básico
            st.dataframe(df_display, use_container_width=True)

    def _render_products_table(self):
        """Renderiza tabela de produtos das OS filtradas"""
        # Verificar se há OS selecionadas
        os_ids = st.session_state.os_selected_ids

        if not os_ids:
            return

        st.markdown("---")
        st.subheader("📦 Produtos das OS")

        try:
            from core.models.modelos import OS_Produtos

            # Buscar produtos das OS selecionadas
            produtos_queryset = OS_Produtos.objects.filter(OS__id__in=os_ids)

            # Converter para lista de dicionários
            produtos_data = list(
                produtos_queryset.values(
                    "OS__id",
                    "OS__ID_Gestao",
                    "Nome",
                    "SiglaUnidade",
                    "Quantidade",
                    "ValorVenda",
                    "TipoDesconto",
                    "Desconto",
                    "DescontoPorcentagem",
                    "ValorTotal",
                )
            )

            if not produtos_data:
                st.info("ℹ️ Nenhum produto encontrado para as OS selecionadas")
                return

            # Converter para DataFrame
            df_produtos = pd.DataFrame(produtos_data)

            # Renomear colunas (INVERTIDO - igual grid de OS)
            column_mapping = {
                "OS__id": "OS Código",
                "OS__ID_Gestao": "ID_OS",
                "Nome": "Produto",
                "SiglaUnidade": "Un.",
                "Quantidade": "Qtd",
                "ValorVenda": "Valor Unit.",
                "TipoDesconto": "Tipo Desc.",
                "Desconto": "Desconto R$",
                "DescontoPorcentagem": "Desconto %",
                "ValorTotal": "Valor Total",
            }

            df_produtos = df_produtos.rename(columns=column_mapping)

            # Formatar valores numéricos
            if "Qtd" in df_produtos.columns:
                df_produtos["Qtd"] = pd.to_numeric(
                    df_produtos["Qtd"], errors="coerce"
                ).fillna(0)

            for col in ["Valor Unit.", "Desconto R$", "Desconto %", "Valor Total"]:
                if col in df_produtos.columns:
                    df_produtos[col] = pd.to_numeric(
                        df_produtos[col], errors="coerce"
                    ).fillna(0)

            # Mostrar informações
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Produtos", len(df_produtos))
            with col2:
                total_geral = (
                    df_produtos["Valor Total"].sum()
                    if "Valor Total" in df_produtos.columns
                    else 0
                )
                st.metric(
                    "Valor Total Geral",
                    f"R$ {total_geral:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                )

            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_produtos)

            gb.configure_grid_options(
                domLayout="normal",
                enableRangeSelection=True,
                enableCellTextSelection=True,
                suppressRowClickSelection=True,
            )

            # Configurações de coluna padrão
            gb.configure_default_column(
                filter=True,
                cellStyle={"border": "1px solid black"},
                floatingFilter=True,
                sortable=True,
            )

            # Configuração personalizada por coluna
            for col in df_produtos.columns:
                if col == "OS Código":
                    gb.configure_column(col, headerName="OS Código", width=120)
                elif col == "ID_OS":
                    gb.configure_column(col, headerName="ID_OS", width=150, hide=True)
                elif col == "Produto":
                    gb.configure_column(col, headerName="Produto", width=250)
                elif col == "Un.":
                    gb.configure_column(col, headerName="Un.", width=80)
                elif col == "Qtd":
                    gb.configure_column(
                        col,
                        headerName="Qtd",
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 2})",
                        width=100,
                    )
                elif col in ["Valor Unit.", "Desconto R$", "Valor Total"]:
                    gb.configure_column(
                        col,
                        headerName=col,
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})",
                        width=130,
                    )
                elif col == "Desconto %":
                    gb.configure_column(
                        col,
                        headerName="Desconto %",
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '%'",
                        width=120,
                    )
                elif col == "Tipo Desc.":
                    gb.configure_column(col, headerName="Tipo Desc.", width=100)

            grid_options = gb.build()

            # Gerar chave única baseada nos dados para forçar atualização
            import hashlib

            produtos_key = hashlib.md5(
                str(df_produtos.values.tolist()).encode()
            ).hexdigest()[:8]

            # Renderizar AgGrid com chave dinâmica
            AgGrid(
                df_produtos,
                gridOptions=grid_options,
                height=400,
                fit_columns_on_grid_load=True,
                theme="alpine",
                allow_unsafe_jscode=True,
                update_mode="MODEL_CHANGED",
                key=f"produtos_grid_{produtos_key}",
            )

            # Seção de download
            st.markdown("---")
            st.subheader("📥 Download dos Produtos")
            col1, col2 = st.columns(2)

            with col1:
                # Download CSV
                csv_data = df_produtos.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"produtos_os_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col2:
                # Download Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df_produtos.to_excel(writer, index=False, sheet_name="Produtos")

                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"produtos_os_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True,
                )

        except ImportError:
            st.error(
                "❌ AgGrid não está instalado. Instale com: pip install streamlit-aggrid"
            )
        except Exception as e:
            st.error(f"❌ Erro ao exibir produtos: {str(e)}")
            self.logger.error(f"Erro ao renderizar grid de produtos: {str(e)}")


def main(key=None):
    """
    Função principal do módulo de OS (compatível com app.py)

    Args:
        key: Chave única para o módulo (requerido pela aplicação principal)
    """
    try:
        # Criar e executar controller
        controller = OSController()
        controller.render_dashboard()

    except Exception as e:
        st.error("❌ Erro fatal no módulo de OS")
        st.error(str(e))
        logging.error(f"Erro fatal no módulo de OS: {str(e)}")


# Para execução direta (desenvolvimento)
if __name__ == "__main__":
    main()
