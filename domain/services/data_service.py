"""
Serviço de dados refatorado para SGR
Implementa lógica de negócio com injeção de dependências
"""

import logging
from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from core.error_handler import handle_errors
from core.exceptions import DatabaseError, ValidationError
from domain.repositories.interfaces import DatabaseRepositoryInterface
from domain.validators import DatabaseQueryParams

logger = logging.getLogger(__name__)


class DataServiceInterface(ABC):
    """Interface para o serviço de dados"""

    @abstractmethod
    def get_data(self, table_name: str, fields: List[str]) -> pd.DataFrame:
        """
        Obtém dados de uma tabela específica

        Args:
            table_name: Nome da tabela
            fields: Lista de campos a serem selecionados

        Returns:
            DataFrame com os dados
        """
        pass


class DataService(DataServiceInterface):
    """
    Serviço principal para operações de dados
    Implementa lógica de negócio e validação
    """

    def __init__(self, repository: DatabaseRepositoryInterface):
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    @handle_errors(show_details=False)
    def get_data(self, table_name: str, fields: List[str]) -> pd.DataFrame:
        """
        Obtém dados com validação

        Args:
            table_name: Nome da tabela
            fields: Lista de campos

        Returns:
            DataFrame com os dados validados

        Raises:
            ValidationError: Se os parâmetros são inválidos
            DatabaseError: Se há erro na consulta
        """
        try:
            # Validar parâmetros de entrada
            params = DatabaseQueryParams(table_name=table_name, fields=fields)

            self._logger.info(
                "Fetching data from table",
                extra={"table": params.table_name, "fields_count": len(params.fields)},
            )

            # Executar consulta via repository
            result = self._repository.fetch_data(params.table_name, params.fields)

            # Validar resultado
            if result is None:
                raise DatabaseError("Consulta retornou resultado nulo")

            self._logger.info(
                "Data fetched successfully",
                extra={
                    "table": params.table_name,
                    "rows_returned": len(result) if hasattr(result, "__len__") else 0,
                },
            )

            return result

        except Exception as e:
            if isinstance(e, (ValidationError, DatabaseError)):
                raise

            self._logger.error(
                "Unexpected error in get_data",
                exc_info=True,
                extra={"table": table_name, "fields": fields},
            )

            raise DatabaseError(
                f"Erro inesperado ao buscar dados da tabela {table_name}",
                details={"original_error": str(e)},
            )

    def validate_table_access(self, table_name: str) -> bool:
        """
        Valida se a tabela pode ser acessada

        Args:
            table_name: Nome da tabela

        Returns:
            True se o acesso é permitido
        """
        # Lista de tabelas permitidas (whitelist)
        allowed_tables = [
            "Clientes",
            "Produtos",
            "Extratos",
            "BoletosEnviados",
            "Empresas",
            "CentroCustos",
            "Bancos",
        ]

        return table_name in allowed_tables

    def get_table_info(self, table_name: str) -> dict:
        """
        Obtém informações sobre uma tabela

        Args:
            table_name: Nome da tabela

        Returns:
            Dicionário com informações da tabela
        """
        if not self.validate_table_access(table_name):
            raise ValidationError(
                "table_name", f"Acesso à tabela '{table_name}' não é permitido"
            )

        try:
            # Esta seria uma implementação real para obter metadados
            return {
                "table_name": table_name,
                "accessible": True,
                "estimated_rows": 0,  # Placeholder
            }
        except Exception as e:
            raise DatabaseError(
                f"Erro ao obter informações da tabela {table_name}",
                details={"original_error": str(e)},
            )
