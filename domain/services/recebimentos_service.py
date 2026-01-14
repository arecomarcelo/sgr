"""
Serviço de domínio para Recebimentos
Implementa a lógica de negócios para análise de recebimentos
"""

import logging
from datetime import date, datetime
from typing import Any, Dict, Optional

import pandas as pd

from core.exceptions import BusinessLogicError, ValidationError
from infrastructure.database.repositories_recebimentos import RecebimentosRepository

logger = logging.getLogger(__name__)


class RecebimentosService:
    """Serviço para operações de recebimentos"""

    def __init__(self, recebimentos_repository: RecebimentosRepository):
        self.recebimentos_repository = recebimentos_repository

    def get_recebimentos_mes_atual(self) -> pd.DataFrame:
        """
        Obtém recebimentos do mês atual (do primeiro dia do mês até hoje)

        Returns:
            pd.DataFrame: Dados de recebimentos filtrados

        Raises:
            BusinessLogicError: Se não conseguir obter dados
        """
        try:
            hoje = datetime.now()
            data_inicial = datetime(hoje.year, hoje.month, 1).date()
            data_final = hoje.date()

            df = self.recebimentos_repository.get_recebimentos_filtrados(
                data_inicial=data_inicial,
                data_final=data_final,
            )

            return self._processar_dados_recebimentos(df)

        except Exception as e:
            raise BusinessLogicError(
                f"Erro ao obter recebimentos do mês atual: {str(e)}"
            )

    def get_recebimentos_filtrados(
        self,
        data_inicio: date,
        data_fim: date,
    ) -> pd.DataFrame:
        """
        Obtém recebimentos com filtros aplicados

        Args:
            data_inicio: Data inicial do filtro
            data_fim: Data final do filtro

        Returns:
            pd.DataFrame: Dados de recebimentos filtrados

        Raises:
            ValidationError: Se dados de entrada inválidos
            BusinessLogicError: Se erro na lógica de negócio
        """
        try:
            # Validar datas
            if data_inicio > data_fim:
                raise ValidationError(
                    field="data_inicio",
                    message="Data inicial não pode ser maior que data final",
                    value={"data_inicio": data_inicio, "data_fim": data_fim},
                )

            logger.info(
                f"Service: Buscando recebimentos de {data_inicio} até {data_fim}"
            )

            df = self.recebimentos_repository.get_recebimentos_filtrados(
                data_inicial=data_inicio,
                data_final=data_fim,
            )

            logger.info(f"Service: Recebidos {len(df)} registros do repository")

            df_processado = self._processar_dados_recebimentos(df)

            logger.info(f"Service: Após processamento, {len(df_processado)} registros")

            return df_processado

        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"Erro ao filtrar recebimentos: {str(e)}")

    def get_metricas_recebimentos(
        self, df_recebimentos: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Calcula métricas de recebimentos

        Args:
            df_recebimentos: DataFrame com dados de recebimentos

        Returns:
            Dict com métricas calculadas

        Raises:
            BusinessLogicError: Se erro no cálculo
        """
        try:
            if df_recebimentos.empty:
                return {
                    "total_quantidade": 0,
                    "total_valor": 0.0,
                }

            # Calcular métricas
            total_quantidade = len(df_recebimentos)

            # Converter valor para numérico se necessário
            df_recebimentos = df_recebimentos.copy()
            if df_recebimentos["Valor"].dtype == "object":
                df_recebimentos["Valor"] = (
                    df_recebimentos["Valor"]
                    .astype(str)
                    .str.replace(",", ".")
                    .astype(float)
                )

            total_valor = df_recebimentos["Valor"].sum()

            return {
                "total_quantidade": total_quantidade,
                "total_valor": total_valor,
            }

        except Exception as e:
            raise BusinessLogicError(f"Erro ao calcular métricas: {str(e)}")

    def _processar_dados_recebimentos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa e formata dados de recebimentos

        Args:
            df: DataFrame bruto

        Returns:
            DataFrame processado
        """
        if df.empty:
            return df

        df = df.copy()

        # Converter data de vencimento para datetime se necessário
        if "Vencimento" in df.columns:
            if df["Vencimento"].dtype == "object":
                df["Vencimento"] = pd.to_datetime(df["Vencimento"], errors="coerce")
            # Formatar data para exibição
            df["Vencimento"] = df["Vencimento"].dt.strftime("%d/%m/%Y")

        # Garantir que Valor seja numérico
        if "Valor" in df.columns and df["Valor"].dtype == "object":
            df["Valor"] = df["Valor"].astype(str).str.replace(",", ".").astype(float)

        return df
