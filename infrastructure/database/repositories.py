"""
Implementações concretas dos repositórios usando Django ORM - SGR
Migração para usar os modelos Django existentes
"""
import logging
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, F, Q, Value
from django.db.models.functions import Coalesce

import pandas as pd

# Importar modelos Django
from app.models import (
    Bancos,
    BoletosEnviados,
    CentroCustos,
    Clientes,
    Empresas,
    Extratos,
    Produtos,
)
from core.exceptions import DatabaseError, SGRException
from infrastructure.database.base import BaseRepository
from infrastructure.database.interfaces import (
    BoletoRepositoryInterface,
    ClienteRepositoryInterface,
    DatabaseRepositoryInterface,
    ExtratoRepositoryInterface,
    UserRepositoryInterface,
    VendaAtualizacaoRepositoryInterface,
    VendaPagamentoRepositoryInterface,
    VendaRepositoryInterface,
)

logger = logging.getLogger(__name__)


class DatabaseRepository(BaseRepository, DatabaseRepositoryInterface):
    """Repositório genérico usando Django ORM"""

    @handle_errors(show_details=False)
    def fetch_data(self, table_name: str, fields: List[str]) -> pd.DataFrame:
        """
        Busca dados de uma tabela usando Django ORM

        Args:
            table_name: Nome da tabela
            fields: Lista de campos a serem selecionados

        Returns:
            DataFrame com os dados
        """
        try:
            # Mapeamento de tabelas para modelos Django
            table_model_map = {
                "Clientes": Clientes,
                "Extratos": Extratos,
                "BoletosEnviados": BoletosEnviados,
                "Produtos": Produtos,
                "Bancos": Bancos,
                "Empresas": Empresas,
                "CentroCustos": CentroCustos,
            }

            if table_name not in table_model_map:
                raise DatabaseQueryError(
                    query=f"Table: {table_name}",
                    message=f"Tabela não suportada: {table_name}",
                )

            model = table_model_map[table_name]

            logger.info(f"Fetching data from table: {table_name}")

            # Usar Django ORM para buscar dados
            queryset = model.objects.all()
            result = self.to_dataframe(queryset, fields)

            logger.info(f"Query successful: {len(result)} rows returned")
            return result

        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise DatabaseQueryError(
                query=f"SELECT {fields} FROM {table_name}",
                message=f"Erro ao buscar dados da tabela {table_name}: {str(e)}",
            )

    @handle_errors(show_details=False)
    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Executa query SQL bruta usando Django

        Args:
            query: Query SQL
            params: Parâmetros da query

        Returns:
            DataFrame com o resultado
        """
        try:
            logger.info("Executing raw SQL query")

            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()

                result = pd.DataFrame(data, columns=columns)

            logger.info(f"Raw query successful: {len(result)} rows returned")
            return result

        except Exception as e:
            logger.error(f"Raw query execution failed: {str(e)}")
            raise DatabaseQueryError(
                query=query, message=f"Erro ao executar query personalizada: {str(e)}"
            )


class UserRepository(BaseRepository, UserRepositoryInterface):
    """Repositório para operações com usuários usando Django ORM"""

    @handle_errors(show_details=False)
    def get_user(self, username: str) -> Optional[tuple]:
        """Busca usuário por nome de usuário usando Django ORM"""
        try:
            user = User.objects.filter(username=username).first()

            if user:
                logger.info(f"User found: {username}")
                # Converter para tuple para manter compatibilidade
                return (
                    user.id,
                    user.password,
                    user.is_superuser,
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.is_staff,
                    user.is_active,
                    user.date_joined,
                    user.last_login,
                )
            else:
                logger.warning(f"User not found: {username}")
                return None

        except Exception as e:
            logger.error(f"Error fetching user {username}: {str(e)}")
            raise DatabaseQueryError(
                query=f"User.objects.filter(username={username})",
                message=f"Erro ao buscar usuário {username}: {str(e)}",
            )

    @handle_errors(show_details=False)
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Busca permissões de um usuário usando Django ORM"""
        try:
            user = User.objects.get(id=user_id)
            permissions = user.get_all_permissions()

            # Extrair apenas os codenames das permissões
            permission_list = [perm.split(".")[-1] for perm in permissions]
            logger.info(f"Found {len(permission_list)} permissions for user {user_id}")

            return permission_list

        except User.DoesNotExist:
            logger.warning(f"User {user_id} not found")
            return []
        except Exception as e:
            logger.error(f"Error fetching permissions for user {user_id}: {str(e)}")
            raise DatabaseQueryError(
                query=f"User permissions for user_id={user_id}",
                message=f"Erro ao buscar permissões do usuário {user_id}: {str(e)}",
            )

    def validate_credentials(self, username: str, password: str) -> bool:
        """Valida credenciais do usuário usando Django auth"""
        from django.contrib.auth.hashers import check_password

        try:
            user = User.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                logger.info(f"Credentials validated for user: {username}")
                return True

            logger.warning(f"Invalid credentials for user: {username}")
            return False

        except Exception as e:
            logger.error(f"Error validating credentials for {username}: {str(e)}")
            return False


class ClienteRepository(BaseRepository, ClienteRepositoryInterface):
    """Repositório para operações com clientes usando Django ORM"""

    @handle_errors(show_details=False)
    def get_clientes(self) -> pd.DataFrame:
        """Busca todos os clientes usando Django ORM"""
        try:
            # Usar Django ORM com anotações para tratar campos nulos
            from django.db.models import Case, Value, When
            from django.db.models.functions import Coalesce

            queryset = (
                Clientes.objects.annotate(
                    RazaoSocial_display=Coalesce("RazaoSocial", Value("-"))
                )
                .values(
                    "TipoPessoa", "RazaoSocial_display", "Nome", "CNPJ", "CPF", "Email"
                )
                .order_by("RazaoSocial")
            )

            result = pd.DataFrame(list(queryset))

            # Renomear coluna para manter compatibilidade
            if "RazaoSocial_display" in result.columns:
                result.rename(
                    columns={"RazaoSocial_display": "RazaoSocial"}, inplace=True
                )

            logger.info(f"Retrieved {len(result)} clients")
            return result

        except Exception as e:
            logger.error(f"Error fetching clients: {str(e)}")
            raise DatabaseQueryError(
                query="Clientes.objects query",
                message=f"Erro ao buscar clientes: {str(e)}",
            )

    def get_cliente_by_id(self, cliente_id: int) -> Optional[Dict[str, Any]]:
        """Busca cliente por ID usando Django ORM"""
        try:
            cliente = Clientes.objects.filter(id=cliente_id).values().first()

            if cliente:
                logger.info(f"Client found: {cliente_id}")
                return cliente

            logger.warning(f"Client not found: {cliente_id}")
            return None

        except Exception as e:
            logger.error(f"Error fetching client {cliente_id}: {str(e)}")
            raise DatabaseQueryError(
                query=f"Clientes.objects.get(id={cliente_id})",
                message=f"Erro ao buscar cliente {cliente_id}: {str(e)}",
            )

    def search_clientes(self, search_term: str) -> pd.DataFrame:
        """Busca clientes por termo usando Django ORM"""
        try:
            from django.db.models import Q

            queryset = (
                Clientes.objects.filter(
                    Q(Nome__icontains=search_term)
                    | Q(RazaoSocial__icontains=search_term)
                )
                .values("TipoPessoa", "RazaoSocial", "Nome", "CNPJ", "CPF", "Email")
                .order_by("Nome")
            )

            result = pd.DataFrame(list(queryset))
            logger.info(f"Found {len(result)} clients matching '{search_term}'")

            return result

        except Exception as e:
            logger.error(f"Error searching clients: {str(e)}")
            raise DatabaseQueryError(
                query=f"Clientes search for '{search_term}'",
                message=f"Erro ao buscar clientes: {str(e)}",
            )


class ExtratoRepository(BaseRepository, ExtratoRepositoryInterface):
    """Repositório para operações com extratos usando Django ORM"""

    @handle_errors(show_details=False)
    def get_extratos_filtrados(
        self,
        data_inicial: date,
        data_final: date,
        empresas: Optional[List[str]] = None,
        centros_custo: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Busca extratos filtrados usando Django ORM"""
        try:
            queryset = Extratos.objects.select_related(
                "banco", "empresa", "centrocusto"
            ).filter(data__range=[data_inicial, data_final])

            if empresas:
                queryset = queryset.filter(empresa__nome__in=empresas)

            if centros_custo:
                queryset = queryset.filter(centrocusto__descricao__in=centros_custo)

            # Usar values para obter dados específicos com joins
            data = queryset.values(
                "banco__descricao",
                "agencia",
                "conta_corrente",
                "data",
                "documento",
                "historico_descricao",
                "valor",
                "debito_credito",
                "empresa__nome",
                "centrocusto__descricao",
            )

            result = pd.DataFrame(list(data))

            # Renomear colunas para compatibilidade
            if not result.empty:
                result.rename(
                    columns={
                        "banco__descricao": "Banco",
                        "historico_descricao": "Descricao",
                        "debito_credito": "D/C",
                        "empresa__nome": "Empresa",
                        "centrocusto__descricao": "CentroCusto",
                    },
                    inplace=True,
                )

            logger.info(f"Retrieved {len(result)} extracts")
            return result

        except Exception as e:
            logger.error(f"Error fetching extracts: {str(e)}")
            raise DatabaseQueryError(
                query="Extratos.objects query",
                message=f"Erro ao buscar extratos: {str(e)}",
            )

    def get_empresas(self) -> List[str]:
        """Busca lista de empresas usando Django ORM"""
        try:
            empresas = (
                Empresas.objects.filter(nome__isnull=False)
                .values_list("nome", flat=True)
                .distinct()
                .order_by("nome")
            )

            return list(empresas)

        except Exception as e:
            logger.error(f"Error fetching companies: {str(e)}")
            raise DatabaseQueryError(
                query="Empresas.objects query",
                message=f"Erro ao buscar empresas: {str(e)}",
            )

    def get_centros_custo(self) -> List[str]:
        """Busca lista de centros de custo usando Django ORM"""
        try:
            centros = (
                CentroCustos.objects.filter(descricao__isnull=False)
                .values_list("descricao", flat=True)
                .distinct()
                .order_by("descricao")
            )

            return list(centros)

        except Exception as e:
            logger.error(f"Error fetching cost centers: {str(e)}")
            raise DatabaseQueryError(
                query="CentroCustos.objects query",
                message=f"Erro ao buscar centros de custo: {str(e)}",
            )


class BoletoRepository(BaseRepository, BoletoRepositoryInterface):
    """Repositório para operações com boletos usando Django ORM"""

    @handle_errors(show_details=False)
    def get_boletos_filtrados(
        self, data_inicial: date, data_final: date
    ) -> pd.DataFrame:
        """Busca boletos filtrados usando Django ORM"""
        try:
            from datetime import datetime, time

            # Converter dates para datetime para filtro
            data_inicio_dt = datetime.combine(data_inicial, time.min)
            data_fim_dt = datetime.combine(data_final, time.max)

            queryset = BoletosEnviados.objects.filter(
                DataHoraEnvio__range=[data_inicio_dt, data_fim_dt]
            ).values("Nome", "Boleto", "Vencimento", "DataHoraEnvio", "Status")

            result = pd.DataFrame(list(queryset))

            # Renomear para compatibilidade
            if not result.empty:
                result.rename(columns={"DataHoraEnvio": "Envio"}, inplace=True)

            logger.info(f"Retrieved {len(result)} boletos")
            return result

        except Exception as e:
            logger.error(f"Error fetching boletos: {str(e)}")
            raise DatabaseQueryError(
                query="BoletosEnviados.objects query",
                message=f"Erro ao buscar boletos: {str(e)}",
            )

    def get_boleto_by_id(self, boleto_id: str) -> Optional[Dict[str, Any]]:
        """Busca boleto por ID usando Django ORM"""
        try:
            boleto = BoletosEnviados.objects.filter(Boleto=boleto_id).values().first()
            return boleto
        except Exception as e:
            logger.error(f"Error fetching boleto {boleto_id}: {str(e)}")
            return None

    def get_boletos_by_status(self, status: str) -> pd.DataFrame:
        """Busca boletos por status usando Django ORM"""
        try:
            queryset = (
                BoletosEnviados.objects.filter(Status=status)
                .values("Nome", "Boleto", "Vencimento", "DataHoraEnvio", "Status")
                .order_by("-DataHoraEnvio")
            )

            return pd.DataFrame(list(queryset))
        except Exception as e:
            logger.error(f"Error fetching boletos by status {status}: {str(e)}")
            return pd.DataFrame()


class EstoqueRepository(BaseRepository, EstoqueRepositoryInterface):
    """Repositório para operações com estoque usando Django ORM"""

    @handle_errors(show_details=False)
    def get_produtos(self) -> pd.DataFrame:
        """Busca produtos usando Django ORM"""
        try:
            queryset = Produtos.objects.values(
                "CodigoInterno",
                "Descricao",
                "ValorCusto",
                "ValorVenda",
                "EstoqueGalpao",
            ).order_by("Descricao")

            result = pd.DataFrame(list(queryset))

            # Renomear para compatibilidade
            if not result.empty:
                result.rename(columns={"CodigoInterno": "Codigo"}, inplace=True)

            logger.info(f"Retrieved {len(result)} products")
            return result

        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            raise DatabaseQueryError(
                query="Produtos.objects query",
                message=f"Erro ao buscar produtos: {str(e)}",
            )

    def get_produto_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Busca produto por código usando Django ORM"""
        try:
            produto = Produtos.objects.filter(CodigoInterno=codigo).values().first()
            return produto
        except Exception as e:
            logger.error(f"Error fetching product {codigo}: {str(e)}")
            return None

    def search_produtos(self, search_term: str) -> pd.DataFrame:
        """Busca produtos por termo usando Django ORM"""
        try:
            from django.db.models import Q

            queryset = (
                Produtos.objects.filter(
                    Q(Descricao__icontains=search_term)
                    | Q(CodigoInterno__icontains=search_term)
                )
                .values(
                    "CodigoInterno",
                    "Descricao",
                    "ValorCusto",
                    "ValorVenda",
                    "EstoqueGalpao",
                )
                .order_by("Descricao")
            )

            result = pd.DataFrame(list(queryset))
            if not result.empty:
                result.rename(columns={"CodigoInterno": "Codigo"}, inplace=True)

            return result
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return pd.DataFrame()

    def get_produtos_baixo_estoque(self, limite: int = 10) -> pd.DataFrame:
        """Busca produtos com estoque baixo usando Django ORM"""
        try:
            # Converter campos string para int para comparação
            from django.db.models import Case, IntegerField, When
            from django.db.models.functions import Cast

            queryset = (
                Produtos.objects.extra(
                    where=[
                        'CAST("EstoqueGalpao" AS INTEGER) <= %s AND CAST("EstoqueGalpao" AS INTEGER) >= 0'
                    ],
                    params=[limite],
                )
                .values("CodigoInterno", "Descricao", "EstoqueGalpao", "ValorVenda")
                .order_by("EstoqueGalpao", "Descricao")
            )

            result = pd.DataFrame(list(queryset))
            if not result.empty:
                result.rename(columns={"CodigoInterno": "Codigo"}, inplace=True)

            logger.info(f"Found {len(result)} products with low stock")
            return result

        except Exception as e:
            logger.error(f"Error fetching low stock products: {str(e)}")
            return pd.DataFrame()
