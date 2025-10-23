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
    VendaProdutosRepositoryInterface,
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
            """
            params = [data_inicial, data_final]

            # Filtro de vendedores específicos (adicional aos critérios obrigatórios)
            if vendedores:
                placeholders = ",".join(["%s"] * len(vendedores))
                query += f' AND "VendedorNome" IN ({placeholders})'
                params.extend(vendedores)

            # Filtro de situação única (opcional)
            if situacao:
                query += ' AND "SituacaoNome" = %s'
                params.append(situacao)

            # Filtro de situações múltiplas (opcional)
            if situacoes:
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


class VendaProdutosRepository(BaseRepository, VendaProdutosRepositoryInterface):
    """Repositório para operações com produtos de vendas"""

    def get_produtos_por_vendas(
        self,
        venda_ids: Optional[List[str]] = None,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
        excluir_grupos: bool = False,
    ) -> pd.DataFrame:
        """Obtém produtos das vendas com filtros aplicados

        Args:
            excluir_grupos: Se True, exclui produtos dos grupos:
                           'PRODUTOS SEM GRUPO', 'PEÇA DE REPOSIÇÃO', 'ACESSÓRIOS'
        """
        try:
            # Query base para obter produtos com join nas vendas e produtos
            # JOIN ignora cores (PRETO/CINZA) dos nomes em Produtos
            query = """
                SELECT
                    vp.id,
                    vp."Venda_ID",
                    vp."Nome",
                    vp."Detalhes",
                    vp."Quantidade",
                    vp."ValorCusto",
                    vp."ValorVenda",
                    vp."ValorDesconto",
                    vp."ValorTotal",
                    p."CodigoExpedicao",
                    p."NomeGrupo",
                    v."VendedorNome",
                    v."Data",
                    v."SituacaoNome"
                FROM "VendaProdutos" vp
                INNER JOIN "Vendas" v ON vp."Venda_ID" = v."ID_Gestao"
                LEFT JOIN "Produtos" p ON
                    vp."Nome" = REPLACE(REPLACE(p."Nome", ' CINZA', ''), ' PRETO', '')
                WHERE 1=1
            """
            params = []

            # Aplicar filtros de vendas
            if data_inicial and data_final:
                query += ' AND v."Data"::DATE BETWEEN %s AND %s'
                params.extend([data_inicial, data_final])

            if vendedores:
                placeholders = ",".join(["%s"] * len(vendedores))
                query += f' AND v."VendedorNome" IN ({placeholders})'
                params.extend(vendedores)

            if situacoes and len(situacoes) > 0:
                placeholders = ",".join(["%s"] * len(situacoes))
                query += f' AND v."SituacaoNome" IN ({placeholders})'
                params.extend(situacoes)
            # Se situacoes=None ou [], não filtra por situação (busca todas)

            if venda_ids and len(venda_ids) > 0:
                placeholders = ",".join(["%s"] * len(venda_ids))
                query += f' AND vp."Venda_ID" IN ({placeholders})'
                params.extend(venda_ids)

            # Aplicar filtro obrigatório de vendedores ativos
            query += ' AND TRIM(v."VendedorNome") IN (SELECT "Nome" FROM "Vendedores")'

            # Excluir grupos específicos se solicitado
            if excluir_grupos:
                query += """ AND (p."NomeGrupo" IS NULL OR p."NomeGrupo" NOT IN (%s, %s, %s))"""
                params.extend(['PRODUTOS SEM GRUPO', 'PEÇA DE REPOSIÇÃO', 'ACESSÓRIOS'])

            query += ' ORDER BY v."Data" DESC, vp."Nome"'

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            logger.info(f"Retrieved {len(result)} product records")
            return result

        except Exception as e:
            logger.error(f"Error fetching products by sales: {str(e)}")
            raise DatabaseError(f"Erro ao buscar produtos por vendas: {str(e)}")

    def get_produtos_agregados(
        self,
        venda_ids: Optional[List[str]] = None,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém produtos agregados (somatórios) das vendas com filtros aplicados"""
        try:
            # Query simples para obter os dados brutos - agregação será feita no Python
            query = """
                SELECT
                    vp."Nome",
                    p."CodigoExpedicao",
                    p."NomeGrupo",
                    vp."Quantidade",
                    vp."ValorCusto",
                    vp."ValorVenda",
                    vp."ValorDesconto",
                    vp."ValorTotal"
                FROM "VendaProdutos" vp
                INNER JOIN "Vendas" v ON vp."Venda_ID" = v."ID_Gestao"
                LEFT JOIN "Produtos" p ON vp."Nome" = p."Nome"
                WHERE 1=1
            """
            params = []

            # Aplicar os mesmos filtros da query de produtos detalhados
            if data_inicial and data_final:
                query += ' AND v."Data"::DATE BETWEEN %s AND %s'
                params.extend([data_inicial, data_final])

            if vendedores:
                placeholders = ",".join(["%s"] * len(vendedores))
                query += f' AND v."VendedorNome" IN ({placeholders})'
                params.extend(vendedores)

            if situacoes and len(situacoes) > 0:
                placeholders = ",".join(["%s"] * len(situacoes))
                query += f' AND v."SituacaoNome" IN ({placeholders})'
                params.extend(situacoes)
            # Se situacoes=None ou [], não filtra por situação (busca todas)

            if venda_ids and len(venda_ids) > 0:
                placeholders = ",".join(["%s"] * len(venda_ids))
                query += f' AND vp."Venda_ID" IN ({placeholders})'
                params.extend(venda_ids)

            # Aplicar filtro obrigatório de vendedores ativos
            query += ' AND TRIM(v."VendedorNome") IN (SELECT "Nome" FROM "Vendedores")'

            query += ' ORDER BY vp."Nome"'

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                df_raw = pd.DataFrame(data, columns=columns)

            # Processar e agregar os dados no Python
            if df_raw.empty:
                return pd.DataFrame()

            # Limpar e converter valores
            def clean_value(val):
                """Limpa valores que podem estar no formato ('10.00',)"""
                if not val or str(val).strip() == '':
                    return 0.0

                # Converter para string e limpar
                val_str = str(val)
                # Remover tuplas: ('10.00',) -> 10.00
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
                'Quantidade',
                'ValorCusto',
                'ValorVenda',
                'ValorDesconto',
                'ValorTotal',
            ]
            for col in numeric_columns:
                if col in df_raw.columns:
                    df_raw[col] = df_raw[col].apply(clean_value)

            # Agregar por produto
            result = (
                df_raw.groupby(['Nome', 'CodigoExpedicao', 'NomeGrupo'])
                .agg(
                    {
                        'Quantidade': 'sum',
                        'ValorCusto': 'sum',
                        'ValorVenda': 'sum',
                        'ValorDesconto': 'sum',
                        'ValorTotal': 'sum',
                    }
                )
                .reset_index()
            )

            # Renomear colunas
            result.columns = [
                'Nome',
                'CodigoExpedicao',
                'NomeGrupo',
                'TotalQuantidade',
                'TotalValorCusto',
                'TotalValorVenda',
                'TotalValorDesconto',
                'TotalValorTotal',
            ]

            # Ordenar por valor total decrescente
            result = result.sort_values('TotalValorTotal', ascending=False)

            logger.info(f"Retrieved {len(result)} aggregated product records")
            return result

        except Exception as e:
            logger.error(f"Error fetching aggregated products: {str(e)}")
            raise DatabaseError(f"Erro ao buscar produtos agregados: {str(e)}")

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


class VendaConfiguracaoRepository(BaseRepository):
    """Repositório para configurações de vendas"""

    def get_meta_vendas(self) -> Optional[float]:
        """Obtém a meta de vendas configurada

        Returns:
            float: Valor da meta de vendas ou None se não encontrado
        """
        try:
            query = (
                'SELECT "Valor" FROM "VendaConfiguracao" WHERE "Descricao" = %s LIMIT 1'
            )

            with connection.cursor() as cursor:
                cursor.execute(query, ['Meta'])
                result = cursor.fetchone()

                if result and result[0]:
                    # Tentar converter para float
                    try:
                        return float(result[0])
                    except (ValueError, TypeError):
                        logger.warning(f"Valor de meta inválido: {result[0]}")
                        return None

                return None

        except Exception as e:
            logger.error(f"Error fetching sales goal: {str(e)}")
            raise DatabaseError(f"Erro ao buscar meta de vendas: {str(e)}")

    def health_check(self) -> bool:
        """Verifica se a conexão está saudável"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False
