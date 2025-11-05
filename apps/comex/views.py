"""
SGR - Módulo Comex - Produtos Detalhados de Vendas
Exibe produtos vendidos com filtros de data
"""

import calendar
import io
import logging
import traceback
from datetime import date, datetime

import pandas as pd
import streamlit as st

# Imports da aplicação refatorada
try:
    from core.container_vendas import DIContainer
    from core.exceptions import BusinessLogicError, SGRException, ValidationError
    from domain.services.vendas_service import VendasService
    from presentation.components.forms_vendas import ValidationHelper
    from presentation.styles.theme_simple import apply_theme
except ImportError as e:
    st.error(f"❌ Erro crítico de importação: {e}")
    st.stop()


class ComexProdutosController:
    """Controller para exibição de produtos detalhados de vendas"""

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
            self.logger.info("Serviços de vendas (Comex) inicializados com sucesso")

        except Exception as e:
            self.logger.error(f"Erro na inicialização: {str(e)}")
            st.error(f"❌ Erro na inicialização: {str(e)}")
            st.error("Verifique a configuração do banco de dados no arquivo .env")
            st.stop()

    def render_dashboard(self):
        """Renderiza dashboard de produtos detalhados"""
        try:
            # Aplicar tema
            apply_theme()

            # Header
            st.markdown(
                "<h1 style='text-align: center; color: #1E88E5;'>📦 Comex - Produtos Detalhados de Vendas</h1>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            # Verificar saúde do sistema (silencioso)
            if not self._health_check_silent():
                st.error("❌ Erro ao conectar com o banco de dados")
                return

            # Inicializar dados na sessão
            if "comex_produtos_df" not in st.session_state:
                st.session_state.comex_produtos_df = None
                # Carregar dados do mês atual automaticamente
                self._auto_load_current_month()

            # Renderizar filtros e dados
            self._render_filters_and_data()

        except Exception as e:
            self.logger.error(f"Erro no dashboard: {str(e)}")
            self.logger.error(traceback.format_exc())
            st.error("❌ Erro inesperado no dashboard. Verifique os logs.")
            with st.expander(
                "🔍 Detalhes do erro (clique para expandir)", expanded=True
            ):
                st.code(traceback.format_exc())
                st.error(f"Tipo de erro: {type(e).__name__}")
                st.error(f"Mensagem: {str(e)}")

    def _health_check_silent(self) -> bool:
        """Verifica saúde do sistema silenciosamente"""
        try:
            health = self.container.health_check()
            return all(health.values())
        except Exception as e:
            self.logger.error(f"Erro no health check: {str(e)}")
            return False

    def _auto_load_current_month(self):
        """Carrega dados do mês atual automaticamente na inicialização"""
        try:
            # Calcular período do mês atual
            hoje = date.today()
            primeiro_dia = hoje.replace(day=1)

            self.logger.info(f"Carregamento automático: {primeiro_dia} a {hoje}")

            # Carregar dados diretamente
            self._load_produtos_data(primeiro_dia, hoje, auto=True)

        except Exception as e:
            self.logger.error(f"Erro no carregamento automático: {str(e)}")
            # Não mostrar erro ao usuário, apenas log

    def _render_filters_and_data(self):
        """Renderiza filtros e dados de produtos"""
        st.subheader("🔍 Filtros de Período")

        # Seção de filtros
        with st.expander("Configurar Período", expanded=False):
            self._render_filters()

        # Exibir dados
        if (
            st.session_state.comex_produtos_df is not None
            and not st.session_state.comex_produtos_df.empty
        ):
            self._render_data_table()
        else:
            # Mensagem se não houver dados
            st.info(
                "ℹ️ **Carregando dados...**\n\n"
                "Se não houver vendas no período, a tabela permanecerá vazia."
            )

    def _render_filters(self):
        """Renderiza seção de filtros de data"""
        try:
            # Filtros de data
            col1, col2 = st.columns(2)

            with col1:
                data_inicio = st.date_input(
                    "📅 Data Inicial",
                    value=date.today().replace(day=1),
                    format="DD/MM/YYYY",
                    help="Selecione a data inicial do período",
                )

            with col2:
                data_fim = st.date_input(
                    "📅 Data Final",
                    value=date.today(),
                    format="DD/MM/YYYY",
                    help="Selecione a data final do período",
                )

            # Botão de busca
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                if st.button(
                    "🔍 Buscar Produtos", type="primary", use_container_width=True
                ):
                    self._load_produtos_data(data_inicio, data_fim, auto=False)

            with col2:
                if st.button("📅 Mês Atual", use_container_width=True):
                    hoje = date.today()
                    primeiro_dia = hoje.replace(day=1)
                    self._load_produtos_data(primeiro_dia, hoje, auto=False)

        except Exception as e:
            st.error(f"❌ Erro nos filtros: {str(e)}")

    def _load_produtos_data(
        self, data_inicio: date, data_fim: date, auto: bool = False
    ):
        """Carrega produtos diretamente para o período especificado

        Fluxo:
        1. Buscar vendas do período
        2. Extrair IDs das vendas
        3. Buscar produtos das vendas (agregados)
        4. Preencher grid
        """
        try:
            # Validar datas
            if not ValidationHelper.validate_date_range(data_inicio, data_fim):
                return

            # Verificar se período é maior que 365 dias (aviso, não bloqueia)
            diff_days = (data_fim - data_inicio).days
            if diff_days > 365 and not auto:
                st.warning("⚠️ Período muito longo pode afetar a performance")

            # Spinner apenas se não for carregamento automático
            if not auto:
                spinner_ctx = st.spinner("⏳ Buscando vendas e produtos...")
                spinner_ctx.__enter__()
            else:
                spinner_ctx = None

            try:
                # PASSO 1: Buscar vendas do período
                self.logger.info(
                    f"PASSO 1: Buscando vendas de {data_inicio} a {data_fim}"
                )

                df_vendas = self.vendas_service.get_vendas_filtradas(
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    vendedores=None,
                    situacoes=None,
                )

                if df_vendas.empty:
                    if not auto:
                        st.warning(
                            "⚠️ Nenhuma venda encontrada para o período selecionado"
                        )
                    st.session_state.comex_produtos_df = pd.DataFrame()
                    return

                self.logger.info(f"✓ Encontradas {len(df_vendas)} vendas")

                # PASSO 2: Extrair IDs das vendas (ID_Gestao é a coluna correta!)
                self.logger.info("PASSO 2: Extraindo IDs das vendas (ID_Gestao)")

                # PRIORIZAR ID_Gestao - é a chave correta para VendaProdutos.Venda_ID
                venda_ids = []
                if "ID_Gestao" in df_vendas.columns:
                    venda_ids = df_vendas["ID_Gestao"].tolist()
                    self.logger.info("✓ Usando coluna ID_Gestao")
                elif "Id" in df_vendas.columns:
                    venda_ids = df_vendas["Id"].tolist()
                    self.logger.warning("⚠️ Usando coluna Id (pode não ser ID_Gestao)")
                elif "id" in df_vendas.columns:
                    venda_ids = df_vendas["id"].tolist()
                elif "ID" in df_vendas.columns:
                    venda_ids = df_vendas["ID"].tolist()
                elif "VendaId" in df_vendas.columns:
                    venda_ids = df_vendas["VendaId"].tolist()

                # Remover valores nulos e converter para string (banco usa VARCHAR)
                venda_ids = [
                    str(vid).strip()
                    for vid in venda_ids
                    if vid is not None and str(vid).strip() != ""
                ]

                if not venda_ids:
                    if not auto:
                        st.warning(
                            f"⚠️ IDs de vendas não disponíveis\n\n"
                            f"Colunas disponíveis: {', '.join(df_vendas.columns.tolist())}"
                        )
                    st.session_state.comex_produtos_df = pd.DataFrame()
                    return

                self.logger.info(
                    f"✓ {len(venda_ids)} IDs extraídos: {venda_ids[:5]}..."
                )

                # PASSO 3: Buscar produtos das vendas DIRETAMENTE (sem filtros restritivos)
                self.logger.info(
                    f"PASSO 3: Buscando produtos DIRETAMENTE para {len(venda_ids)} vendas"
                )

                # Buscar produtos diretamente do repository, SEM filtros de vendedores ativos
                produtos_detalhados_df = self._buscar_produtos_direto(venda_ids)

                self.logger.info(
                    f"✓ Retornados {len(produtos_detalhados_df)} produtos detalhados"
                )

                if not produtos_detalhados_df.empty:
                    self.logger.info(
                        f"✓ Colunas: {produtos_detalhados_df.columns.tolist()}"
                    )

                if produtos_detalhados_df.empty:
                    if not auto:
                        st.warning(
                            "⚠️ Nenhum produto encontrado para as vendas do período"
                        )
                    st.session_state.comex_produtos_df = pd.DataFrame()
                    return

                # PASSO 3.5: Agregar produtos manualmente
                self.logger.info("PASSO 3.5: Agregando produtos por nome")

                produtos_df = self._agregar_produtos(produtos_detalhados_df)

                self.logger.info(f"✓ {len(produtos_df)} produtos únicos após agregação")

                # PASSO 4: Armazenar e exibir
                st.session_state.comex_produtos_df = produtos_df

                if not auto:
                    st.success(
                        f"✅ {len(produtos_df)} produtos carregados ({len(venda_ids)} vendas)"
                    )
                    st.rerun()
                else:
                    self.logger.info(
                        f"✓ {len(produtos_df)} produtos carregados automaticamente"
                    )

            finally:
                if spinner_ctx:
                    spinner_ctx.__exit__(None, None, None)

        except ValidationError as e:
            st.error(f"❌ Erro de validação: {str(e)}")
            self.logger.error(f"Erro de validação: {str(e)}")
        except BusinessLogicError as e:
            st.error(f"❌ Erro de negócio: {str(e)}")
            self.logger.error(f"Erro de negócio: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar produtos: {str(e)}")
            self.logger.error(f"Erro ao carregar produtos: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _buscar_produtos_direto(self, venda_ids: list) -> pd.DataFrame:
        """Busca produtos diretamente do banco SEM filtros restritivos de vendedores"""
        try:
            from django.db import connection

            if not venda_ids:
                return pd.DataFrame()

            self.logger.info(
                f"_buscar_produtos_direto: Buscando produtos para {len(venda_ids)} IDs"
            )
            self.logger.info(f"Primeiros 3 IDs: {venda_ids[:3]}")

            # Query SQL direta - SIMPLES, sem filtro de vendedores ativos
            # VendaProdutos.Venda_ID = Vendas.ID_Gestao
            placeholders = ",".join(["%s"] * len(venda_ids))
            query = f"""
                SELECT
                    vp."Nome",
                    vp."Quantidade",
                    vp."ValorCusto",
                    vp."ValorVenda",
                    vp."ValorDesconto",
                    vp."ValorTotal",
                    p."CodigoExpedicao",
                    p."NomeGrupo",
                    p."EstoqueGalpao"
                FROM "VendaProdutos" vp
                LEFT JOIN "Produtos" p ON vp."Nome" = p."Nome"
                WHERE vp."Venda_ID" IN ({placeholders})
                ORDER BY vp."Nome"
            """

            self.logger.info(f"Executando query com {len(venda_ids)} parâmetros")

            with connection.cursor() as cursor:
                cursor.execute(query, venda_ids)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                df = pd.DataFrame(data, columns=columns)

            self.logger.info(f"✓ Query direta retornou {len(df)} produtos")
            if len(df) > 0:
                self.logger.info(
                    f"✓ Primeiros 3 produtos: {df['Nome'].head(3).tolist()}"
                )
            else:
                self.logger.error(
                    f"❌ Query retornou 0 produtos para os IDs: {venda_ids[:10]}"
                )

            return df

        except Exception as e:
            self.logger.error(f"Erro na query direta: {str(e)}")
            import traceback

            self.logger.error(traceback.format_exc())
            return pd.DataFrame()

    def _agregar_produtos(self, df_detalhado: pd.DataFrame) -> pd.DataFrame:
        """Agrega produtos detalhados por nome, somando quantidades e valores"""
        try:
            if df_detalhado.empty:
                return pd.DataFrame()

            # Função para limpar valores monetários
            def clean_value(val):
                """Limpa valores que podem estar no formato ('10.00',)"""
                if pd.isna(val) or not val or str(val).strip() == "":
                    return 0.0

                # Se já é número, retornar
                if isinstance(val, (int, float)):
                    return float(val)

                # Converter para string e limpar
                val_str = str(val)
                val_str = (
                    val_str.replace("(", "")
                    .replace(")", "")
                    .replace("'", "")
                    .replace(",", ".")
                )
                val_str = val_str.strip()

                try:
                    return float(val_str) if val_str else 0.0
                except:
                    return 0.0

            # Aplicar limpeza aos campos numéricos
            numeric_columns = [
                "Quantidade",
                "ValorCusto",
                "ValorVenda",
                "ValorDesconto",
                "ValorTotal",
            ]
            for col in numeric_columns:
                if col in df_detalhado.columns:
                    df_detalhado[col] = df_detalhado[col].apply(clean_value)

            # Definir colunas para agrupamento
            group_cols = ["Nome"]
            if "CodigoExpedicao" in df_detalhado.columns:
                group_cols.append("CodigoExpedicao")
            if "NomeGrupo" in df_detalhado.columns:
                group_cols.append("NomeGrupo")

            # Agregar por produto
            agg_dict = {}
            if "Quantidade" in df_detalhado.columns:
                agg_dict["Quantidade"] = "sum"
            if "ValorCusto" in df_detalhado.columns:
                agg_dict["ValorCusto"] = "sum"
            if "ValorVenda" in df_detalhado.columns:
                agg_dict["ValorVenda"] = "sum"
            if "ValorDesconto" in df_detalhado.columns:
                agg_dict["ValorDesconto"] = "sum"
            if "ValorTotal" in df_detalhado.columns:
                agg_dict["ValorTotal"] = "sum"
            # Preservar EstoqueGalpao (usa first pois é um valor único por produto)
            if "EstoqueGalpao" in df_detalhado.columns:
                agg_dict["EstoqueGalpao"] = "first"

            result = df_detalhado.groupby(group_cols).agg(agg_dict).reset_index()

            # Renomear colunas para padrão agregado
            rename_dict = {
                "Quantidade": "TotalQuantidade",
                "ValorCusto": "TotalValorCusto",
                "ValorVenda": "TotalValorVenda",
                "ValorDesconto": "TotalValorDesconto",
                "ValorTotal": "TotalValorTotal",
            }

            result = result.rename(columns=rename_dict)

            # Ordenar por valor total decrescente
            if "TotalValorTotal" in result.columns:
                result = result.sort_values("TotalValorTotal", ascending=False)

            return result

        except Exception as e:
            self.logger.error(f"Erro ao agregar produtos: {str(e)}")
            return pd.DataFrame()

    def _render_data_table(self):
        """Renderiza tabela de produtos usando AgGrid"""
        df = st.session_state.comex_produtos_df

        if df is None or df.empty:
            return

        st.subheader("📋 Produtos Detalhados")

        # Preparar dados para exibição
        try:
            from st_aggrid import AgGrid, GridOptionsBuilder

            # Criar cópia para exibição
            df_display = df.copy()

            # Função para limpar e converter valores monetários
            def clean_monetary_value(val):
                """Remove formatação monetária e converte para float"""
                if pd.isna(val):
                    return 0.0
                if isinstance(val, (int, float)):
                    return float(val)
                # Converter para string e limpar
                val_str = str(val).replace("R$", "").strip()

                # Se tem vírgula, é formato brasileiro (1.500,00)
                if "," in val_str:
                    # Remover pontos (separador de milhares) e trocar vírgula por ponto
                    val_clean = val_str.replace(".", "").replace(",", ".")
                else:
                    # Formato americano ou já limpo (1500.00 ou 1500)
                    val_clean = val_str

                val_clean = val_clean.strip()
                try:
                    return float(val_clean) if val_clean else 0.0
                except:
                    return 0.0

            # Garantir que valores monetários sejam float (sem formatação)
            for col in df_display.columns:
                if "Valor" in col or "Preco" in col or "Custo" in col:
                    df_display[col] = df_display[col].apply(clean_monetary_value)

            # Reordenar colunas para que Estoque fique entre Quantidade e Custo
            cols = df_display.columns.tolist()
            if "EstoqueGalpao" in cols and "TotalQuantidade" in cols:
                # Remover EstoqueGalpao da posição atual
                cols.remove("EstoqueGalpao")
                # Encontrar posição após TotalQuantidade
                idx_quantidade = cols.index("TotalQuantidade")
                # Inserir EstoqueGalpao após TotalQuantidade
                cols.insert(idx_quantidade + 1, "EstoqueGalpao")
                # Reordenar DataFrame
                df_display = df_display[cols]

            # Função para formatar valores no padrão brasileiro (europeu)
            def format_br_number(valor, decimals=2):
                """Formata número no padrão brasileiro: ponto para milhares, vírgula para decimais"""
                if decimals == 0:
                    return f"{valor:,.0f}".replace(",", ".")
                else:
                    formatted = f"{valor:,.{decimals}f}"
                    # Trocar vírgula por ponto (milhares) e ponto por vírgula (decimais)
                    formatted = (
                        formatted.replace(",", "X").replace(".", ",").replace("X", ".")
                    )
                    return formatted

            # Calcular totais para métricas
            total_qtd = 0
            total_valor = 0.0

            if "TotalQuantidade" in df_display.columns:
                total_qtd = df_display["TotalQuantidade"].sum()
            elif "Quantidade" in df_display.columns:
                total_qtd = df_display["Quantidade"].sum()

            if "TotalValorTotal" in df_display.columns:
                total_valor = df_display["TotalValorTotal"].sum()
            elif "ValorTotal" in df_display.columns:
                total_valor = df_display["ValorTotal"].sum()

            # Mostrar informações do dataset e botões de download
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1, 1])

            with col1:
                st.metric("📦 Total Produtos", len(df_display))
            with col2:
                st.metric("📊 Quantidade Total", format_br_number(total_qtd, 0))
            with col3:
                st.metric("💰 Valor Total", f"R$ {format_br_number(total_valor, 2)}")
            with col4:
                # Botão Excel
                buffer_excel = io.BytesIO()
                with pd.ExcelWriter(buffer_excel, engine="xlsxwriter") as writer:
                    df_display.to_excel(writer, index=False, sheet_name="Produtos")

                st.download_button(
                    label="📊 Excel",
                    data=buffer_excel.getvalue(),
                    file_name=f"comex_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            with col5:
                # Botão CSV
                csv_data = df_display.to_csv(index=False)
                st.download_button(
                    label="📄 CSV",
                    data=csv_data,
                    file_name=f"comex_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            st.markdown("---")

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
                if "Valor" in col or "Preco" in col or "Custo" in col:
                    # Colunas monetárias com formatação europeia/brasileira
                    header_name = col.replace("Total", "").replace("Valor", "").strip()
                    if not header_name:
                        header_name = "Valor"
                    gb.configure_column(
                        col,
                        headerName=header_name,
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="'R$ ' + x.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})",
                        width=150,
                    )
                elif "Quantidade" in col:
                    gb.configure_column(
                        col,
                        headerName="Quantidade",
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 0})",
                        width=130,
                    )
                elif col in ["EstoqueGalpao", "Estoque"]:
                    # Nova coluna de estoque
                    gb.configure_column(
                        col,
                        headerName="Estoque",
                        type=["numericColumn", "numberColumnFilter"],
                        valueFormatter="x.toLocaleString('pt-BR', {minimumFractionDigits: 0, maximumFractionDigits: 0})",
                        width=120,
                    )
                elif col in ["Nome", "ProdutoNome"]:
                    gb.configure_column(col, headerName="Produto", width=350)
                elif col in ["CodigoExpedicao", "ProdutoCodigo"]:
                    gb.configure_column(col, headerName="Código", width=150)
                elif col == "NomeGrupo":
                    gb.configure_column(col, headerName="Grupo", width=200)
                else:
                    gb.configure_column(col, headerName=col, width=150)

            grid_options = gb.build()

            # Renderizar AgGrid
            grid_response = AgGrid(
                df_display,
                gridOptions=grid_options,
                height=500,
                fit_columns_on_grid_load=True,
                theme="alpine",
                allow_unsafe_jscode=True,
                update_mode="MODEL_CHANGED",
                key="comex_produtos_grid",
            )

        except ImportError:
            st.error(
                "❌ AgGrid não está instalado. Instale com: pip install streamlit-aggrid"
            )
            # Fallback: mostrar dataframe básico
            st.dataframe(df.head(100), use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erro ao exibir tabela: {str(e)}")
            self.logger.error(f"Erro ao renderizar grid: {str(e)}")
            self.logger.error(traceback.format_exc())
            # Fallback: mostrar dataframe básico
            st.dataframe(df.head(100), use_container_width=True)


def main(key=None):
    """
    Função principal do módulo Comex (compatível com app.py)

    Args:
        key: Chave única para o módulo (requerido pela aplicação principal)
    """
    try:
        # Criar e executar controller
        controller = ComexProdutosController()
        controller.render_dashboard()

    except Exception as e:
        st.error("❌ Erro fatal no módulo Comex")
        st.error(str(e))
        logging.error(f"Erro fatal no módulo Comex: {str(e)}")


# Para execução direta (desenvolvimento)
if __name__ == "__main__":
    main()
