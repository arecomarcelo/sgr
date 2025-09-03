"""
Repositórios específicos para Vendas usando Django ORM com SQL bruto
"""
import logging
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional

from django.db import connection

import pandas as pd

from core.exceptions import DatabaseError
from infrastructure.database.base import BaseRepository
from infrastructure.database.interfaces import (
    VendaAtualizacaoRepositoryInterface,
    VendaPagamentoRepositoryInterface,
    VendaRepositoryInterface,
)

logger = logging.getLogger(__name__)


class VendaRepository(BaseRepository, VendaRepositoryInterface):
    """Repositório para operações com vendas usando SQL bruto via Django"""

    def get_vendas_filtradas(
        self,
        data_inicial: date,
        data_final: date,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
        situacao: Optional[str] = None,
        apenas_vendedores_ativos: bool = False,
    ) -> pd.DataFrame:
        """Obtém vendas com filtros aplicados usando SQL bruto"""
        try:
            # Query base com critérios obrigatórios aplicados SEMPRE
            query = """
                SELECT * FROM "Vendas"
                WHERE "Data"::DATE BETWEEN %s AND %s
                AND TRIM("VendedorNome") IN (SELECT "Nome" FROM "Vendedores")
                AND "SituacaoNome" = 'Em andamento'
            """
            params = [data_inicial, data_final]

            # Filtro de vendedores específicos (adicional aos critérios obrigatórios)
            if vendedores:
                placeholders = ",".join(["%s"] * len(vendedores))
                query += f' AND "VendedorNome" IN ({placeholders})'
                params.extend(vendedores)

            # Filtro de situação única (sobrescreve o critério obrigatório se especificado)
            if situacao:
                # Remove o filtro obrigatório de situação e aplica o específico
                query = query.replace('AND "SituacaoNome" = \'Em andamento\'', '')
                query += ' AND "SituacaoNome" = %s'
                params.append(situacao)

            # Filtro de situações múltiplas (sobrescreve o critério obrigatório se especificado)
            if situacoes:
                # Remove o filtro obrigatório de situação e aplica os específicos
                query = query.replace('AND "SituacaoNome" = \'Em andamento\'', '')
                placeholders = ",".join(["%s"] * len(situacoes))
                query += f' AND "SituacaoNome" IN ({placeholders})'
                params.extend(situacoes)

            query += ' ORDER BY "Data" DESC'

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            logger.info(f"Retrieved {len(result)} sales records")
            return result

        except Exception as e:
            logger.error(f"Error fetching filtered sales: {str(e)}")
            raise DatabaseError(f"Erro ao buscar vendas filtradas: {str(e)}")

    def get_vendedores_ativos(self) -> pd.DataFrame:
        """Obtém lista de vendedores ativos"""
        try:
            query = 'SELECT DISTINCT "Nome" as "VendedorNome" FROM "Vendedores" ORDER BY "Nome"'

            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            return result

        except Exception as e:
            logger.error(f"Error fetching active sellers: {str(e)}")
            raise DatabaseError(f"Erro ao buscar vendedores ativos: {str(e)}")

    def get_situacoes_disponiveis(self) -> pd.DataFrame:
        """Obtém situações de venda disponíveis"""
        try:
            query = 'SELECT DISTINCT "SituacaoNome" FROM "Vendas" WHERE "SituacaoNome" IS NOT NULL ORDER BY "SituacaoNome"'

            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            return result

        except Exception as e:
            logger.error(f"Error fetching available statuses: {str(e)}")
            raise DatabaseError(f"Erro ao buscar situações disponíveis: {str(e)}")

    def health_check(self) -> bool:
        """Verifica se a conexão está saudável"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False


class VendaPagamentoRepository(BaseRepository, VendaPagamentoRepositoryInterface):
    """Repositório para operações com pagamentos de vendas"""

    def get_pagamentos_por_vendas(self, venda_ids: List[str]) -> pd.DataFrame:
        """Obtém pagamentos por IDs de vendas"""
        try:
            if not venda_ids:
                return pd.DataFrame()

            placeholders = ",".join(["%s"] * len(venda_ids))
            query = f"""
                SELECT * FROM "VendaPagamentos"
                WHERE "Venda_ID" IN ({placeholders})
                ORDER BY "DataVencimento"
            """

            with connection.cursor() as cursor:
                cursor.execute(query, venda_ids)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            logger.info(f"Retrieved {len(result)} payment records")
            return result

        except Exception as e:
            logger.error(f"Error fetching payments by sales: {str(e)}")
            raise DatabaseError(f"Erro ao buscar pagamentos por vendas: {str(e)}")

    def get_pagamentos_filtrados(
        self,
        data_inicial: date,
        data_final: date,
        venda_ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém pagamentos com filtros aplicados"""
        try:
            query = """
                SELECT * FROM "VendaPagamentos"
                WHERE "DataVencimento"::DATE BETWEEN %s AND %s
            """
            params = [data_inicial, data_final]

            if venda_ids:
                placeholders = ",".join(["%s"] * len(venda_ids))
                query += f' AND "Venda_ID" IN ({placeholders})'
                params.extend(venda_ids)

            query += ' ORDER BY "DataVencimento"'

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            return result

        except Exception as e:
            logger.error(f"Error fetching filtered payments: {str(e)}")
            raise DatabaseError(f"Erro ao buscar pagamentos filtrados: {str(e)}")

    def health_check(self) -> bool:
        """Verifica se a conexão está saudável"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False


class VendaAtualizacaoRepository(BaseRepository, VendaAtualizacaoRepositoryInterface):
    """Repositório para informações de atualização de vendas"""

    def get_ultima_atualizacao(self) -> pd.DataFrame:
        """Obtém informações da última atualização"""
        try:
            query = 'SELECT * FROM "VendaAtualizacao" ORDER BY "Data" DESC, "Hora" DESC LIMIT 1'

            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            return result

        except Exception as e:
            logger.error(f"Error fetching last update info: {str(e)}")
            raise DatabaseError(f"Erro ao buscar informações de atualização: {str(e)}")

    def get_historico_atualizacoes(self, limite: int = 10) -> pd.DataFrame:
        """Obtém histórico de atualizações"""
        try:
            query = 'SELECT * FROM "VendaAtualizacao" ORDER BY "Data" DESC, "Hora" DESC LIMIT %s'

            with connection.cursor() as cursor:
                cursor.execute(query, [limite])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            return result

        except Exception as e:
            logger.error(f"Error fetching update history: {str(e)}")
            raise DatabaseError(f"Erro ao buscar histórico de atualizações: {str(e)}")

    def health_check(self) -> bool:
        """Verifica se a conexão está saudável"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False
