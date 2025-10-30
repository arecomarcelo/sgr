"""
Interfaces dos repositórios para SGR
Define contratos para acesso a dados seguindo padrão Repository
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd


class BaseRepositoryInterface(ABC):
    """Interface base para todos os repositórios"""

    @abstractmethod
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        pass


class DatabaseRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações genéricas no banco de dados"""

    @abstractmethod
    def fetch_data(self, table_name: str, fields: List[str]) -> pd.DataFrame:
        """
        Busca dados de uma tabela específica

        Args:
            table_name: Nome da tabela
            fields: Lista de campos a serem selecionados

        Returns:
            DataFrame com os dados
        """
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Executa uma query personalizada

        Args:
            query: Query SQL
            params: Parâmetros da query

        Returns:
            DataFrame com o resultado
        """
        pass


class UserRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações com usuários"""

    @abstractmethod
    def get_user(self, username: str) -> Optional[tuple]:
        """
        Busca usuário por nome de usuário

        Args:
            username: Nome do usuário

        Returns:
            Tuple com dados do usuário ou None se não encontrado
        """
        pass

    @abstractmethod
    def get_user_permissions(self, user_id: int) -> List[str]:
        """
        Busca permissões de um usuário

        Args:
            user_id: ID do usuário

        Returns:
            Lista de permissões
        """
        pass

    @abstractmethod
    def validate_credentials(self, username: str, password: str) -> bool:
        """
        Valida credenciais do usuário

        Args:
            username: Nome do usuário
            password: Senha do usuário

        Returns:
            True se credenciais válidas
        """
        pass


class ClienteRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações com clientes"""

    @abstractmethod
    def get_clientes(self) -> pd.DataFrame:
        """
        Busca todos os clientes

        Returns:
            DataFrame com dados dos clientes
        """
        pass

    @abstractmethod
    def get_cliente_by_id(self, cliente_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca cliente por ID

        Args:
            cliente_id: ID do cliente

        Returns:
            Dicionário com dados do cliente ou None
        """
        pass

    @abstractmethod
    def search_clientes(self, search_term: str) -> pd.DataFrame:
        """
        Busca clientes por termo

        Args:
            search_term: Termo de busca

        Returns:
            DataFrame com clientes encontrados
        """
        pass


class ExtratoRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações com extratos"""

    @abstractmethod
    def get_extratos_filtrados(
        self,
        data_inicial: date,
        data_final: date,
        empresas: Optional[List[str]] = None,
        centros_custo: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Busca extratos filtrados por período e critérios

        Args:
            data_inicial: Data inicial do filtro
            data_final: Data final do filtro
            empresas: Lista de empresas (opcional)
            centros_custo: Lista de centros de custo (opcional)

        Returns:
            DataFrame com extratos filtrados
        """
        pass

    @abstractmethod
    def get_empresas(self) -> List[str]:
        """
        Busca lista de empresas disponíveis

        Returns:
            Lista de nomes das empresas
        """
        pass

    @abstractmethod
    def get_centros_custo(self) -> List[str]:
        """
        Busca lista de centros de custo disponíveis

        Returns:
            Lista de centros de custo
        """
        pass


class BoletoRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações com boletos"""

    @abstractmethod
    def get_boletos_filtrados(
        self, data_inicial: date, data_final: date
    ) -> pd.DataFrame:
        """
        Busca boletos filtrados por período

        Args:
            data_inicial: Data inicial do filtro
            data_final: Data final do filtro

        Returns:
            DataFrame com boletos filtrados
        """
        pass

    @abstractmethod
    def get_boleto_by_id(self, boleto_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca boleto por ID

        Args:
            boleto_id: ID do boleto

        Returns:
            Dicionário com dados do boleto ou None
        """
        pass

    @abstractmethod
    def get_boletos_by_status(self, status: str) -> pd.DataFrame:
        """
        Busca boletos por status

        Args:
            status: Status do boleto

        Returns:
            DataFrame com boletos do status especificado
        """
        pass


class EstoqueRepositoryInterface(BaseRepositoryInterface):
    """Interface para operações com estoque"""

    @abstractmethod
    def get_produtos(self) -> pd.DataFrame:
        """
        Busca todos os produtos do estoque

        Returns:
            DataFrame com dados dos produtos
        """
        pass

    @abstractmethod
    def get_produto_by_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        """
        Busca produto por código

        Args:
            codigo: Código do produto

        Returns:
            Dicionário com dados do produto ou None
        """
        pass

    @abstractmethod
    def search_produtos(self, search_term: str) -> pd.DataFrame:
        """
        Busca produtos por termo

        Args:
            search_term: Termo de busca

        Returns:
            DataFrame com produtos encontrados
        """
        pass

    @abstractmethod
    def get_produtos_baixo_estoque(self, limite: int = 10) -> pd.DataFrame:
        """
        Busca produtos com estoque baixo

        Args:
            limite: Limite mínimo de estoque

        Returns:
            DataFrame com produtos em estoque baixo
        """
        pass
