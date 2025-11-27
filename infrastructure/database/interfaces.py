"""
Interfaces para repositórios
Define contratos para implementação de repositórios
"""

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pandas as pd


class BaseRepositoryInterface(ABC):
    """Interface base para repositórios"""

    @abstractmethod
    def health_check(self) -> bool:
        """Verifica se a conexão está saudável"""
        pass


class VendaRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de vendas"""

    @abstractmethod
    def get_vendas_filtradas(
        self,
        data_inicial: date,
        data_final: date,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
        situacao: Optional[str] = None,
        situacoes_excluir: Optional[List[str]] = None,
        apenas_vendedores_ativos: bool = False,
    ) -> pd.DataFrame:
        """Obtém vendas com filtros aplicados"""
        pass

    @abstractmethod
    def get_vendedores_ativos(self) -> pd.DataFrame:
        """Obtém lista de vendedores ativos"""
        pass

    @abstractmethod
    def get_situacoes_disponiveis(self) -> pd.DataFrame:
        """Obtém situações de venda disponíveis"""
        pass


class VendaProdutosRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de produtos de vendas"""

    @abstractmethod
    def get_produtos_por_vendas(
        self,
        venda_ids: Optional[List[str]] = None,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém produtos das vendas com filtros aplicados"""
        pass

    @abstractmethod
    def get_produtos_agregados(
        self,
        venda_ids: Optional[List[str]] = None,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None,
        vendedores: Optional[List[str]] = None,
        situacoes: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém produtos agregados (somatórios) das vendas com filtros aplicados"""
        pass


class VendaPagamentoRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de pagamentos de vendas"""

    @abstractmethod
    def get_pagamentos_por_vendas(self, venda_ids: List[str]) -> pd.DataFrame:
        """Obtém pagamentos por IDs de vendas"""
        pass

    @abstractmethod
    def get_pagamentos_filtrados(
        self,
        data_inicial: date,
        data_final: date,
        venda_ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém pagamentos com filtros aplicados"""
        pass


class VendaAtualizacaoRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de atualizações de vendas"""

    @abstractmethod
    def get_ultima_atualizacao(self) -> pd.DataFrame:
        """Obtém informações da última atualização"""
        pass

    @abstractmethod
    def get_historico_atualizacoes(self, limite: int = 10) -> pd.DataFrame:
        """Obtém histórico de atualizações"""
        pass


class ClienteRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de clientes"""

    @abstractmethod
    def get_clientes(self) -> pd.DataFrame:
        """Obtém todos os clientes"""
        pass

    @abstractmethod
    def get_cliente_por_id(self, cliente_id: str) -> pd.DataFrame:
        """Obtém cliente por ID"""
        pass


class ExtratoRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de extratos"""

    @abstractmethod
    def get_extratos_filtrados(
        self,
        data_inicial: date,
        data_final: date,
        empresas: Optional[List[str]] = None,
        centros_custo: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Obtém extratos com filtros aplicados"""
        pass


class BoletoRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de boletos"""

    @abstractmethod
    def get_boletos_filtrados(
        self, data_inicial: date, data_final: date
    ) -> pd.DataFrame:
        """Obtém boletos com filtros aplicados"""
        pass


class UserRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório de usuários"""

    @abstractmethod
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtém usuário por username"""
        pass

    @abstractmethod
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Obtém permissões do usuário"""
        pass


class DatabaseRepositoryInterface(BaseRepositoryInterface):
    """Interface para repositório genérico de banco de dados"""

    @abstractmethod
    def fetch_data(self, table_name: str, campos: List[str]) -> pd.DataFrame:
        """Obtém dados de uma tabela específica"""
        pass

    @abstractmethod
    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """Executa query personalizada"""
        pass
