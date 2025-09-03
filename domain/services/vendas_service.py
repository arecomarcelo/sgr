"""
Serviço de domínio para Vendas
Implementa a lógica de negócios para análise de vendas
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from core.exceptions import BusinessLogicError, SGRException, ValidationError
from domain.validators_simple import DateRangeValidator, VendasFilterValidator
from infrastructure.database.repositories_vendas import (
    VendaAtualizacaoRepository,
    VendaPagamentoRepository,
    VendaRepository,
)


class VendasService:
    """Serviço para operações de vendas"""

    def __init__(
        self,
        venda_repository: VendaRepository,
        pagamento_repository: VendaPagamentoRepository,
        atualizacao_repository: VendaAtualizacaoRepository,
    ):
        self.venda_repository = venda_repository
        self.pagamento_repository = pagamento_repository
        self.atualizacao_repository = atualizacao_repository

    def get_vendas_mes_atual(self) -> pd.DataFrame:
        """
        Obtém vendas do mês atual com filtros de negócio aplicados
        Se hoje for dia 1, retorna dados do mês anterior
        Aplica critério rígido: VendedorNome IN (SELECT Nome FROM Vendedores) AND SituacaoNome = 'Em andamento'

        Returns:
            pd.DataFrame: Dados de vendas filtrados

        Raises:
            BusinessLogicError: Se não conseguir obter dados
        """
        try:
            hoje = datetime.now()

            # SEMPRE usar mês atual: dia 1 até dia atual
            data_inicial = datetime(hoje.year, hoje.month, 1).date()
            data_final = hoje.date()

            # Os critérios obrigatórios são aplicados automaticamente no repositório
            df = self.venda_repository.get_vendas_filtradas(
                data_inicial=data_inicial,
                data_final=data_final,
            )

            return self._processar_dados_vendas(df)

        except Exception as e:
            raise BusinessLogicError(f"Erro ao obter vendas do mês atual: {str(e)}")

    def get_vendas_filtradas(
        self,
        data_inicio: datetime,
        data_fim: datetime,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Obtém vendas com filtros aplicados

        Args:
            data_inicio: Data inicial do filtro
            data_fim: Data final do filtro
            vendedores: Lista de vendedores (opcional)
            situacoes: Lista de situações (opcional)

        Returns:
            pd.DataFrame: Dados de vendas filtrados

        Raises:
            ValidationError: Se dados de entrada inválidos
            BusinessLogicError: Se erro na lógica de negócio
        """
        try:
            # Validar entrada
            filtros = VendasFilterValidator(
                data_inicio=data_inicio,
                data_fim=data_fim,
                vendedores=vendedores or [],
                situacoes=situacoes or [],
            )

            # Validar range de datas
            date_range = DateRangeValidator(start_date=data_inicio, end_date=data_fim)

            df = self.venda_repository.get_vendas_filtradas(
                data_inicial=filtros.data_inicio,
                data_final=filtros.data_fim,
                vendedores=filtros.vendedores,
                situacoes=filtros.situacoes,
            )

            return self._processar_dados_vendas(df)

        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"Erro ao filtrar vendas: {str(e)}")

    def get_metricas_vendas(self, df_vendas: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula métricas de vendas

        Args:
            df_vendas: DataFrame com dados de vendas

        Returns:
            Dict com métricas calculadas

        Raises:
            BusinessLogicError: Se erro no cálculo
        """
        try:
            if df_vendas.empty:
                return {
                    "total_quantidade": 0,
                    "total_valor": 0.0,
                    "ticket_medio": 0.0,
                    "margem_media": 0.0,
                }

            # Obter pagamentos relacionados
            ids_vendas = df_vendas["ID_Gestao"].tolist()
            df_pagamentos = self.pagamento_repository.get_pagamentos_por_vendas(
                ids_vendas
            )

            # Calcular métricas
            total_quantidade = len(df_vendas)
            total_valor = df_vendas["ValorTotal"].sum()
            ticket_medio = df_vendas["ValorTotal"].mean()

            # Calcular entrada e parcelado
            entradas = 0.0
            parcelado = 0.0

            if not df_pagamentos.empty:
                # Processar dados de pagamentos
                df_pagamentos = df_pagamentos.copy()

                # Converter colunas de valor para float
                if "Valor" in df_pagamentos.columns:
                    df_pagamentos["Valor"] = df_pagamentos["Valor"].astype(str)
                    df_pagamentos["Valor"] = (
                        df_pagamentos["Valor"].str.replace(",", ".").astype(float)
                    )

                # Converter DataVencimento para datetime se for string
                if "DataVencimento" in df_pagamentos.columns:
                    df_pagamentos["DataVencimento"] = pd.to_datetime(
                        df_pagamentos["DataVencimento"], errors="coerce"
                    )

                # Calcular entrada e parcelado
                hoje = datetime.now()
                entradas = df_pagamentos[df_pagamentos["DataVencimento"] <= hoje][
                    "Valor"
                ].sum()

                parcelado = df_pagamentos[df_pagamentos["DataVencimento"] > hoje][
                    "Valor"
                ].sum()

            # Calcular margem se houver dados de custo
            margem_media = 0.0
            if "ValorCusto" in df_vendas.columns and df_vendas["ValorCusto"].sum() > 0:
                custo_total = df_vendas["ValorCusto"].sum()
                margem_media = ((total_valor - custo_total) / total_valor) * 100

            return {
                "total_quantidade": total_quantidade,
                "total_valor": total_valor,
                "total_entradas": entradas,
                "total_parcelado": parcelado,
                "ticket_medio": ticket_medio,
                "margem_media": margem_media,
            }

        except Exception as e:
            raise BusinessLogicError(f"Erro ao calcular métricas: {str(e)}")

    def get_vendas_por_vendedor(
        self, df_vendas: pd.DataFrame, top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Agrupa vendas por vendedor

        Args:
            df_vendas: DataFrame com dados de vendas
            top_n: Número máximo de vendedores (opcional)

        Returns:
            pd.DataFrame: Dados agregados por vendedor
        """
        try:
            if df_vendas.empty:
                return pd.DataFrame()

            vendas_por_vendedor = (
                df_vendas.groupby("VendedorNome")
                .agg(
                    total_valor=("ValorTotal", "sum"),
                    quantidade=("ValorTotal", "count"),
                    ticket_medio=("ValorTotal", "mean"),
                )
                .reset_index()
            )

            # Ordenar por valor total
            vendas_por_vendedor = vendas_por_vendedor.sort_values(
                "total_valor", ascending=False
            )

            # Limitar se especificado
            if top_n and len(vendas_por_vendedor) > top_n:
                vendas_por_vendedor = vendas_por_vendedor.head(top_n)

            return vendas_por_vendedor

        except Exception as e:
            raise BusinessLogicError(f"Erro ao agrupar por vendedor: {str(e)}")

    def get_tendencia_vendas(
        self, df_vendas: pd.DataFrame, periodo: str = "mes"
    ) -> pd.DataFrame:
        """
        Calcula tendência de vendas por período

        Args:
            df_vendas: DataFrame com dados de vendas
            periodo: Tipo de período ('dia', 'semana', 'mes')

        Returns:
            pd.DataFrame: Dados de tendência
        """
        try:
            if df_vendas.empty:
                return pd.DataFrame()

            df_copy = df_vendas.copy()
            df_copy["Data"] = pd.to_datetime(df_copy["Data"])

            # Definir agrupamento por período
            if periodo == "dia":
                df_copy["Periodo"] = df_copy["Data"].dt.strftime("%Y-%m-%d")
            elif periodo == "semana":
                df_copy["Periodo"] = df_copy["Data"].dt.strftime("%Y-W%U")
            else:  # mes
                df_copy["Periodo"] = df_copy["Data"].dt.strftime("%Y-%m")

            # Agrupar por período
            tendencia = (
                df_copy.groupby("Periodo")
                .agg(
                    valor_total=("ValorTotal", "sum"),
                    quantidade=("ValorTotal", "count"),
                    ticket_medio=("ValorTotal", "mean"),
                )
                .reset_index()
            )

            return tendencia

        except Exception as e:
            raise BusinessLogicError(f"Erro ao calcular tendência: {str(e)}")

    def get_informacoes_atualizacao(self) -> Dict[str, Any]:
        """
        Obtém informações da última atualização

        Returns:
            Dict com informações de atualização
        """
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
            raise BusinessLogicError(
                f"Erro ao obter informações de atualização: {str(e)}"
            )

    def get_vendedores_ativos(self) -> List[str]:
        """
        Obtém lista de vendedores ativos

        Returns:
            List[str]: Lista de nomes dos vendedores
        """
        try:
            df = self.venda_repository.get_vendedores_ativos()
            return sorted(df["VendedorNome"].unique().tolist())
        except Exception as e:
            raise BusinessLogicError(f"Erro ao obter vendedores: {str(e)}")

    def get_situacoes_disponiveis(self) -> List[str]:
        """
        Obtém lista de situações de venda disponíveis

        Returns:
            List[str]: Lista de situações
        """
        try:
            df = self.venda_repository.get_situacoes_disponiveis()
            return sorted(df["SituacaoNome"].unique().tolist())
        except Exception as e:
            raise BusinessLogicError(f"Erro ao obter situações: {str(e)}")

    def _processar_dados_vendas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa e limpa dados de vendas

        Args:
            df: DataFrame bruto de vendas

        Returns:
            pd.DataFrame: DataFrame processado
        """
        if df.empty:
            return df

        # Fazer cópia para evitar modificar original
        df = df.copy()

        # Converter colunas de valores
        valor_columns = ["ValorTotal", "ValorDesconto", "ValorProdutos", "ValorCusto"]
        for col in valor_columns:
            if col in df.columns:
                # Garantir que seja string antes de processar
                df[col] = df[col].astype(str)
                # Tratar valores vazios - apenas para ValorTotal que é obrigatório
                if col == "ValorTotal":
                    # Remover linhas com ValorTotal vazio (obrigatório)
                    df = df[df[col].str.strip() != ""]
                else:
                    # Para outros campos, substituir vazios por "0"
                    df[col] = df[col].apply(
                        lambda x: "0" if not x or str(x).strip() == "" else str(x)
                    )
                # Converter vírgula para ponto e para float
                df[col] = df[col].str.replace(",", ".").astype(float)

        # Converter colunas de data
        date_columns = ["Data"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

    def formatar_valor_monetario(self, valor: float) -> str:
        """
        Formata valor como moeda brasileira

        Args:
            valor: Valor numérico

        Returns:
            str: Valor formatado
        """
        return f"R$ {valor:,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")
