import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from dotenv import load_dotenv
import locale
import io  # Importando a biblioteca io para manipulação de buffers

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para aplicar o CSS personalizado
def apply_custom_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1E88E5;
        }
        .metric-label {
            font-size: 1rem;
            color: #6c757d;
            margin-top: 0.5rem;
        }
        .filter-section {
            background-color: #f1f3f5;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .chart-container {
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        th {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# Aplicar o CSS personalizado
apply_custom_css()

# Carregando variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Classe para manipulação de dados
class DataService:
    def __init__(self, connection_string):
        """
        Inicializa o serviço de dados com a string de conexão
        
        Args:
            connection_string (str): String de conexão SQLAlchemy para o PostgreSQL
        """
        self.connection_string = connection_string
        self.engine = None
        
    def connect(self):
        """
        Estabelece a conexão com o banco de dados
        
        Returns:
            bool: True se a conexão for bem-sucedida, False caso contrário
        """
        try:
            self.engine = create_engine(self.connection_string)
            return True
        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def get_vendas_data(self):
        """
        Obtém todos os dados da tabela de Vendas
        
        Returns:
            pandas.DataFrame: DataFrame com os dados de vendas
        """
        try:
            query = "SELECT * FROM \"Vendas\""
            df = pd.read_sql_query(text(query), self.engine)
            
            # Convertendo colunas de valores para float
            valor_columns = ['ValorTotal', 'DescontoValor', 'ValorProdutos', 'ValorCusto']
            for col in valor_columns:
                df = df[df[col].str.strip() != ''] # Remove linhas com strings vazias
                df[col] = df[col].str.replace(',', '.').astype(float) # Converte para float
                
            # Convertendo colunas de data para datetime
            date_columns = ['Data', 'PrevisaoEntrega', 'DataPrimeiraParcela']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            
            return df
        except Exception as e:
            st.error(f"Erro ao obter dados de vendas: {e}")
            return pd.DataFrame()
    
    def get_pagamentos_data(self):
        """
        Obtém todos os dados da tabela de Pagamentos
        
        Returns:
            pandas.DataFrame: DataFrame com os dados de pagamentos
        """
        try:
            query = "SELECT * FROM \"VendaPagamentos\""
            df = pd.read_sql_query(text(query), self.engine)
            
            # Convertendo colunas de valores para float
            valor_columns = ['Valor']
            for col in valor_columns:
                df = df[df[col].str.strip() != ''] # Remove linhas com strings vazias
                df[col] = df[col].str.replace(',', '.').astype(float) # Converte para float
                
            # Convertendo colunas de data para datetime
            date_columns = ['DataVencimento']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            
            return df
        except Exception as e:
            st.error(f"Erro ao obter dados de pagamentos: {e}")
            return pd.DataFrame()
    
    def get_vendedores(self, df):
        """
        Obtém a lista de vendedores
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
            
        Returns:
            list: Lista de vendedores
        """
        return sorted(df['VendedorNome'].unique().tolist())
    
    def get_situacoes(self, df):
        """
        Obtém a lista de situações de venda
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
            
        Returns:
            list: Lista de situações
        """
        return sorted(df['SituacaoNome'].unique().tolist())
    
    def formatar_valor(self, valor):
        """
        Formata um valor numérico como moeda brasileira
        
        Args:
            valor (float): Valor a ser formatado
            
        Returns:
            str: Valor formatado
        """
        return f"R${valor:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')  # Formatação para moeda
    
    def prepare_data_pizza_vendedores(self, df, mes_atual=True):
        """
        Prepara os dados para o gráfico de pizza de vendas por vendedor
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
            mes_atual (bool): Flag para filtrar apenas o mês atual
            
        Returns:
            pandas.DataFrame: DataFrame agregado por vendedor
        """
        # Filtra para o mês atual se solicitado
        if mes_atual:
            hoje = datetime.now()
            primeiro_dia_mes = datetime(hoje.year, hoje.month, 1)
            ultimo_dia_mes = primeiro_dia_mes + pd.offsets.MonthEnd(0)
            df = df[(df['Data'] >= primeiro_dia_mes) & (df['Data'] <= ultimo_dia_mes)]
        
        # Agrupa por vendedor
        vendas_por_vendedor = df.groupby('VendedorNome').agg(
            total_valor=('ValorTotal', 'sum'),
            quantidade=('ValorTotal', 'count')
        ).reset_index()
        
        # Ordena por valor total
        vendas_por_vendedor = vendas_por_vendedor.sort_values('total_valor', ascending=False)
        
        return vendas_por_vendedor
    
    def prepare_data_colunas_empilhadas(self, df):
        """
        Prepara os dados para o gráfico de colunas empilhadas de quantidade e valor
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
            
        Returns:
            pandas.DataFrame: DataFrame formatado para gráfico de colunas empilhadas
        """
        # Agrupa por vendedor
        vendas_por_vendedor = df.groupby('VendedorNome').agg(
            total_valor=('ValorTotal', 'sum'),
            quantidade=('ValorTotal', 'count')
        ).reset_index()
        
        # Ordena por valor total (descendente)
        vendas_por_vendedor = vendas_por_vendedor.sort_values('total_valor', ascending=False)
        
        # Normaliza os valores para obter uma visualização proporcional
        max_valor = vendas_por_vendedor['total_valor'].max()
        max_qtd = vendas_por_vendedor['quantidade'].max()
        
        # Adiciona colunas normalizadas (opcional, pode ser usado para visualizações alternativas)
        vendas_por_vendedor['valor_normalizado'] = vendas_por_vendedor['total_valor'] / max_valor * 100
        vendas_por_vendedor['qtd_normalizada'] = vendas_por_vendedor['quantidade'] / max_qtd * 100
        
        return vendas_por_vendedor

    def get_atualizacao_data(self):
        """
        Obtém os dados de atualização da tabela VendaAtualizacao
        
        Returns:
            pandas.DataFrame: DataFrame com os dados de atualização
        """
        try:
            query = "SELECT * FROM \"VendaAtualizacao\" LIMIT 1"
            df = pd.read_sql_query(text(query), self.engine)
            return df
        except Exception as e:
            st.error(f"Erro ao obter dados de atualização: {e}")
            return pd.DataFrame()

# Classe para visualização de dados
class DashboardView:
    def __init__(self, data_service):
        """
        Inicializa a visualização do dashboard
        
        Args:
            data_service (DataService): Serviço de dados
        """
        self.data_service = data_service
        self.configure_locale()

    def configure_locale(self):
        """Configura localização para formato brasileiro"""
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'C')  
        finally:
            apply_custom_css()
    
    def render_filters(self, df):
        """
        Renderiza os filtros do dashboard
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
        
        Returns:
            tuple: Tupla com os filtros selecionados (data_inicio, data_fim, vendedor, situacao)
        """
        # Aplicar CSS novamente antes de renderizar os filtros
        apply_custom_css()
        
        st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
        st.subheader("Filtros")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtro de data inicial usando widget padrão
            hoje = datetime.now()
            primeiro_dia_mes = datetime(hoje.year, hoje.month, 1)
            data_min = primeiro_dia_mes.date()
            data_inicio = st.date_input("Data Inicial:", value=data_min, min_value=data_min, max_value=datetime.now().date(), format="DD/MM/YYYY")
        
        with col2:
            # Filtro de data final usando widget padrão
            data_max = (datetime.now() - timedelta(days=1)).date()
            data_fim = st.date_input("Data Final:", value=data_max, min_value=data_min, max_value=data_max, format="DD/MM/YYYY")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Filtro de vendedor
            vendedores = self.data_service.get_vendedores(df)
            vendedor = st.multiselect("Vendedor:", options=vendedores, default=[])
        
        with col4:
            # Filtro de situação
            situacoes = self.data_service.get_situacoes(df)
            situacao = st.multiselect("Situação:", options=situacoes, default=[])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        return data_inicio, data_fim, vendedor, situacao
    
    def apply_filters(self, df, data_inicio, data_fim, vendedor, situacao):
        """
        Aplica os filtros ao DataFrame
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
            data_inicio (date): Data de início do período
            data_fim (date): Data de fim do período
            vendedor (list): Lista de vendedores selecionados
            situacao (list): Lista de situações selecionadas
            
        Returns:
            pandas.DataFrame: DataFrame filtrado
        """
        # Filtro de data
        df_filtered = df[(df['Data'].dt.date >= data_inicio) & 
                         (df['Data'].dt.date <= data_fim)]
        
        # Filtro de vendedor
        if vendedor:
            df_filtered = df_filtered[df_filtered['VendedorNome'].isin(vendedor)]
        
        # Filtro de situação
        if situacao:
            df_filtered = df_filtered[df_filtered['SituacaoNome'].isin(situacao)]
        
        return df_filtered
    
    def render_metrics(self, df_filtered, df_pagamentos):
            """
            Renderiza as métricas principais do dashboard com base nos filtros aplicados
            
            Args:
                df_filtered (pandas.DataFrame): DataFrame filtrado com os dados de vendas
                df_pagamentos (pandas.DataFrame): DataFrame com os dados de pagamentos
            """
            st.markdown("<h2 class='main-header'>Métricas de Vendas</h2>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_qtd = len(df_filtered)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_qtd}</div>
                    <div class="metric-label">Total de Vendas (Quantidade)</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Filtrando pagamentos com base nos IDs de vendas filtradas
            df_pagamentos_filtrados = df_pagamentos[df_pagamentos['Venda_ID'].isin(df_filtered['ID_Gestao'])]
            
            with col2:
                entradas = df_pagamentos_filtrados[df_pagamentos_filtrados['DataVencimento'] <= datetime.now()]['Valor'].sum()
                entrada_formatado = self.data_service.formatar_valor(entradas)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{entrada_formatado}</div>
                    <div class="metric-label">Total de Entrada (Valor)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                parcelado = df_pagamentos_filtrados[df_pagamentos_filtrados['DataVencimento'] > datetime.now()]['Valor'].sum()
                parcelado_formatado = self.data_service.formatar_valor(parcelado)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{parcelado_formatado}</div>
                    <div class="metric-label">Total Parcelado (Valor)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                total_valor = entradas + parcelado
                total_valor_formatado = self.data_service.formatar_valor(total_valor)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_valor_formatado}</div>
                    <div class="metric-label">Total de Vendas (Valor)</div>
                </div>
                """, unsafe_allow_html=True)    

    def render_charts(self, df):
        """
        Renderiza os gráficos de análise de vendedores (pizza e colunas empilhadas)
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
        """
        # Aplicar CSS novamente antes de renderizar os gráficos
        apply_custom_css()
        
        st.markdown("<h2 class='main-header'>Análise de Vendedores</h2>", unsafe_allow_html=True)
        
        # Se não houver dados, exibe mensagem e retorna
        if df.empty:
            st.warning("Não há dados disponíveis para exibir os gráficos.")
            return
        
        # Criar layout de duas colunas para os gráficos
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Distribuição de Vendas por Vendedor")
        
        # Preparar dados para o gráfico de pizza
        vendas_por_vendedor = self.data_service.prepare_data_pizza_vendedores(df, False)
        
        # Criar gráfico de pizza
        fig = px.pie(
            vendas_por_vendedor,
            values='total_valor',
            names='VendedorNome',
            title='Vendas por Vendedor (Valor)',
            color_discrete_sequence=px.colors.sequential.Blues,
            hole=0.4
        )
        
        # Atualizar o layout do gráfico
        fig.update_layout(
            legend_title="Vendedores",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            margin=dict(t=50, b=100, l=10, r=10),
            height=450
        )
        
        # Atualizar texto das legendas para incluir valores
        new_labels = []
        for i, vendedor in enumerate(vendas_por_vendedor['VendedorNome']):
            valor = vendas_por_vendedor.iloc[i]['total_valor']
            qtd = vendas_por_vendedor.iloc[i]['quantidade']
            valor_fmt = self.data_service.formatar_valor(valor)
            new_labels.append(f"{vendedor}: {valor_fmt} ({qtd} vendas)")
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Valor: %{value:.2f}<br>Porcentagem: %{percent}',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Quantidade de Vendas por Vendedor")
        
        # Preparar dados para o gráfico de colunas empilhadas
        dados = self.data_service.prepare_data_colunas_empilhadas(df)
        
        # Limitar para os top 10 vendedores por valor total para melhor visualização
        if len(dados) > 10:
            dados = dados.head(10)
        
        # Criar figura com eixos secundários
        fig = go.Figure()
        
        # Adicionar barras para quantidade
        fig.add_trace(
            go.Bar(
                x=dados['VendedorNome'],
                y=dados['quantidade'],
                name='Quantidade',
                marker_color='#4CAF50',
                hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<br>',
                text=dados['quantidade'],
                textposition='auto'
            )
        )
        
        # Atualizar layout com eixos duplos
        fig.update_layout(
            title='Quantidade de Vendas por Vendedor',
            xaxis=dict(
                title='Vendedor',
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title='Quantidade',
                titlefont=dict(color='#4CAF50'),
                tickfont=dict(color='#4CAF50')
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            barmode='group',
            height=450,
            margin=dict(t=100, b=100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Valor Total de Vendas por Vendedor")
        
        # Preparar dados para o gráfico de colunas empilhadas
        dados = self.data_service.prepare_data_colunas_empilhadas(df)
        
        # Limitar para os top 10 vendedores por valor total para melhor visualização
        if len(dados) > 10:
            dados = dados.head(10)
        
        # Criar figura com eixos secundários
        fig = go.Figure()
        
        # Adicionar barras para valores
        fig.add_trace(
            go.Bar(
                x=dados['VendedorNome'],
                y=dados['total_valor'],
                name='Valor Total',
                marker_color='#1E88E5',
                hovertemplate='<b>%{x}</b><br>Valor: %{y:.2f}<br>',
                text=[self.data_service.formatar_valor(valor) for valor in dados['total_valor']],
                textposition='auto'
            )
        )
        
        # Atualizar layout com eixos duplos
        fig.update_layout(
            title='Valor Total de Vendas por Vendedor',
            xaxis=dict(
                title='Vendedor',
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title='Valor Total (R$)',
                titlefont=dict(color='#1E88E5'),
                tickfont=dict(color='#1E88E5')
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            barmode='group',
            height=450,
            margin=dict(t=100, b=100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_grid(self, df):
        """
        Renderiza um grid com os campos: ClienteNome, VendedorNome, ValorProdutos, DescontoValor e ValorTotal
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
        """
        with st.expander("Dados da Venda"):
            # Selecionar apenas as colunas necessárias
            df_grid = df[['ClienteNome', 'VendedorNome', 'ValorProdutos', 'DescontoValor', 'ValorTotal']]
            
            # Renomear as colunas para os cabeçalhos desejados
            df_grid.columns = ['Cliente', 'Vendedor', 'Valor Venda', 'Desconto', 'Valor Total']
            
            # Formatando valores para moeda brasileira
            df_grid['Valor Venda'] = df_grid['Valor Venda'].apply(lambda x: self.data_service.formatar_valor(x))
            df_grid['Desconto'] = df_grid['Desconto'].apply(lambda x: self.data_service.formatar_valor(x))
            df_grid['Valor Total'] = df_grid['Valor Total'].apply(lambda x: self.data_service.formatar_valor(x))
            
            # Renderizar o grid usando st.dataframe para manter o mesmo estilo da sessão "Detalhes Adicionais"
            st.dataframe(df_grid, height=300)
            
            # Botão para download dos dados em Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_grid.to_excel(writer, index=False, sheet_name='Dados_Venda')
                writer.close()  # Usando close() em vez de save()
                buffer.seek(0)
            
            st.download_button(
                label="📥 Download dos Dados (Excel)",
                data=buffer,
                file_name=f"dados_venda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.ms-excel"
            )
    
    def render_additional_info(self, df):
        """
        Renderiza informações adicionais úteis para análise
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados de vendas
        """
        # Aplicar CSS novamente antes de renderizar informações adicionais
        apply_custom_css()
        
        with st.expander("Detalhes Adicionais"):
            # Criar abas para diferentes visualizações
            tab1, tab2, tab3 = st.tabs(["Tabela de Dados", "Métricas Avançadas", "Tendências"])
            
            with tab1:
                st.dataframe(df, height=300)
                
                # Botão para download dos dados em Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Dados_Completos')
                    writer.close()  # Usando close() em vez de save()
                    buffer.seek(0)
                
                st.download_button(
                    label="📥 Download dos Dados (Excel)",
                    data=buffer,
                    file_name=f"dados_completos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
            
            with tab2:
                if not df.empty:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Ticket médio
                        ticket_medio = df['ValorTotal'].mean()
                        st.metric("Ticket Médio", self.data_service.formatar_valor(ticket_medio))
                        
                    with col2:
                        # Margem média (assumindo ValorCusto como custo)
                        if 'ValorCusto' in df.columns:
                            margem_total = ((df['ValorTotal'].sum() - df['ValorCusto'].sum()) / df['ValorTotal'].sum()) * 100
                            st.metric("Margem Média", f"{margem_total:.2f}%")
                    
                    with col3:
                        # Desconto médio
                        df = df[df['DescontoPorcentagem'].str.strip() != ''] # Remove linhas com strings vazias
                        desconto_medio = df['DescontoPorcentagem'].astype(float).mean()  
                        st.metric("Desconto Médio", f"{desconto_medio:.2f}%")
            
            with tab3:
                if not df.empty:
                    # Agrupar por data
                    pd.options.mode.chained_assignment = None # Desativa o aviso

                    df['Data'] = pd.to_datetime(df['Data'])

                    # Usando .loc[] para evitar o erro
                    df.loc[:, 'Mês'] = df['Data'].dt.strftime('%Y-%m')                    

                    vendas_por_mes = df.groupby('Mês').agg(
                        valor_total=('ValorTotal', 'sum'),
                        quantidade=('ValorTotal', 'count')
                    ).reset_index()
                    
                    # Criar gráfico de linha
                    fig = px.line(
                        vendas_por_mes, 
                        x='Mês', 
                        y='valor_total',
                        markers=True,
                        title='Tendência de Vendas ao Longo do Tempo'
                    )
                    st.plotly_chart(fig, use_container_width=True)

    def render_atualizacao_info(self):
        """
        Renderiza o painel de informações de atualização
        """
        # Obter dados de atualização
        df_atualizacao = self.data_service.get_atualizacao_data()
        
        if df_atualizacao.empty:
            st.warning("Não há dados de atualização disponíveis.")
            return
        
        # Extrair os valores da última atualização
        data = df_atualizacao.iloc[0]['Data']
        hora = df_atualizacao.iloc[0]['Hora']
        periodo = df_atualizacao.iloc[0]['Periodo']
        inseridos = df_atualizacao.iloc[0]['Inseridos']
        atualizados = df_atualizacao.iloc[0]['Atualizados']
        
        # Renderizar os cards
        st.markdown("<h2 class='main-header'>Informações de Atualização</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data}</div>
                <div class="metric-label">Data</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{hora}</div>
                <div class="metric-label">Hora</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{periodo}</div>
                <div class="metric-label">Período</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{inseridos}</div>
                <div class="metric-label">Inseridos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{atualizados}</div>
                <div class="metric-label">Atualizados</div>
            </div>
            """, unsafe_allow_html=True)

def iniciar_dashboard(connection_string):
    """
    Inicializa e renderiza o dashboard
    
    Args:
        connection_string (str): String de conexão com o banco de dados
    """
    # Título do dashboard
    st.markdown("<h1 class='main-header'>Dashboard de Análise de Vendas</h1>", unsafe_allow_html=True)

    # Inicializar serviço de dados
    data_service = DataService(connection_string)
    
    # Conectar ao banco de dados
    if not data_service.connect():
        st.error("Falha ao conectar ao banco de dados. Verifique as configurações.")
        return
    
    # Obter dados de vendas
    loading_message = st.empty()
    loading_message.info("Carregando dados de vendas...")
    df_vendas = data_service.get_vendas_data()
    loading_message.empty()
    
    if df_vendas.empty:
        st.error("Não foi possível obter dados de vendas. Verifique se a tabela existe.")
        return
    
    # Obter dados de pagamentos
    loading_message = st.empty()
    loading_message.info("Carregando dados de pagamentos...")
    df_pagamentos = data_service.get_pagamentos_data()
    loading_message.empty()
    
    if df_pagamentos.empty:
        st.error("Não foi possível obter dados de pagamentos. Verifique se a tabela existe.")
        return
    
    # Inicializar visualização
    dashboard_view = DashboardView(data_service)
    
    # Renderizar painel de atualização
    dashboard_view.render_atualizacao_info()
    
    # Renderizar filtros
    data_inicio, data_fim, vendedor, situacao = dashboard_view.render_filters(df_vendas)
    
    # Aplicar filtros
    df_filtrado = dashboard_view.apply_filters(df_vendas, data_inicio, data_fim, vendedor, situacao)
    
    # Renderizar métricas
    dashboard_view.render_metrics(df_filtrado, df_pagamentos)
    
    # Renderizar gráficos (agora com método unificado que inclui ambos os gráficos)
    dashboard_view.render_charts(df_filtrado)
    
    # Renderizar grid
    dashboard_view.render_grid(df_filtrado)
    
    # Renderizar informações adicionais
    dashboard_view.render_additional_info(df_filtrado)

# Função principal
def main():
    # Verificar se as variáveis de ambiente estão definidas
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        st.error("""
        Configurações de banco de dados não encontradas. Por favor, configure o arquivo .env com:
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
        """)
        
        # Formulário para inserção manual
        with st.form("database_config"):
            st.subheader("Configuração Manual do Banco de Dados")
            
            temp_user = st.text_input("Usuário:", value=DB_USER or "")
            temp_password = st.text_input("Senha:", type="password", value=DB_PASSWORD or "")
            temp_host = st.text_input("Host:", value=DB_HOST or "localhost")
            temp_port = st.text_input("Porta:", value=DB_PORT or "5432")
            temp_name = st.text_input("Nome do Banco:", value=DB_NAME or "")
            
            submit = st.form_submit_button("Conectar")
            
            if submit:
                connection_string = f"postgresql://{temp_user}:{temp_password}@{temp_host}:{temp_port}/{temp_name}"
                iniciar_dashboard(connection_string)
        
        return
    
    # Criar string de conexão e iniciar dashboard
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    iniciar_dashboard(connection_string)    

if __name__ == "__main__":
    main()