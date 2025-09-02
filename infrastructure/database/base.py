"""
Classe base para repositórios
Implementa funcionalidades comuns para todos os repositórios
"""
import logging
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class BaseRepository:
    """Classe base para todos os repositórios"""

    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        """
        Inicializa repositório base

        Args:
            db_config: Configuração do banco de dados (opcional para Django ORM)
        """
        self.db_config = db_config

    def to_dataframe(
        self, queryset, fields: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Converte QuerySet Django para DataFrame pandas

        Args:
            queryset: QuerySet do Django
            fields: Campos específicos para selecionar

        Returns:
            pd.DataFrame: DataFrame convertido
        """
        try:
            if fields:
                data = list(queryset.values(*fields))
            else:
                data = list(queryset.values())

            return pd.DataFrame(data)

        except Exception as e:
            logger.error(f"Erro ao converter QuerySet para DataFrame: {str(e)}")
            raise Exception(f"Erro na conversão de dados: {str(e)}")

    def health_check(self) -> bool:
        """
        Verifica se a conexão com o banco está saudável

        Returns:
            bool: True se conexão está OK
        """
        try:
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False

    def log_query_performance(
        self, query_name: str, duration: float, record_count: int
    ):
        """
        Log de performance de queries

        Args:
            query_name: Nome da query
            duration: Duração em segundos
            record_count: Número de registros retornados
        """
        logger.info(
            f"Query '{query_name}' executada em {duration:.3f}s, "
            f"retornou {record_count} registros"
        )
