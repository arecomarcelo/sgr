"""
Factory para criação de repositórios - SGR
Implementa padrão Factory para instanciar repositórios
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Type, cast

from config.settings import DatabaseConfig
from core.exceptions import ConfigurationError
from domain.repositories.interfaces import (
    BaseRepositoryInterface,
    BoletoRepositoryInterface,
    ClienteRepositoryInterface,
    DatabaseRepositoryInterface,
    EstoqueRepositoryInterface,
    ExtratoRepositoryInterface,
    UserRepositoryInterface,
)


class RepositoryType(Enum):
    """Enum para tipos de repositório disponíveis"""

    DATABASE = "database"
    USER = "user"
    CLIENTE = "cliente"
    EXTRATO = "extrato"
    BOLETO = "boleto"
    ESTOQUE = "estoque"


class RepositoryFactoryInterface(ABC):
    """Interface para factories de repositório"""

    @abstractmethod
    def create(self, repo_type: RepositoryType, **kwargs) -> BaseRepositoryInterface:
        """
        Cria uma instância de repositório

        Args:
            repo_type: Tipo do repositório
            **kwargs: Argumentos adicionais

        Returns:
            Instância do repositório
        """
        pass

    @abstractmethod
    def is_supported(self, repo_type: RepositoryType) -> bool:
        """
        Verifica se o tipo de repositório é suportado

        Args:
            repo_type: Tipo do repositório

        Returns:
            True se suportado
        """
        pass


class DatabaseRepositoryFactory(RepositoryFactoryInterface):
    """
    Factory para repositórios de banco de dados PostgreSQL
    Cria instâncias baseadas em configuração de banco
    """

    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self._repository_registry: Dict[
            RepositoryType, Type[BaseRepositoryInterface]
        ] = {}
        self._setup_registry()

    def _setup_registry(self):
        """Configura o registro de repositórios disponíveis"""
        # Import local para evitar dependências circulares
        from infrastructure.database.repositories import (
            BoletoRepository,
            ClienteRepository,
            DatabaseRepository,
            EstoqueRepository,
            ExtratoRepository,
            UserRepository,
        )

        self._repository_registry = {
            RepositoryType.DATABASE: DatabaseRepository,
            RepositoryType.USER: UserRepository,
            RepositoryType.CLIENTE: ClienteRepository,
            RepositoryType.EXTRATO: ExtratoRepository,
            RepositoryType.BOLETO: BoletoRepository,
            RepositoryType.ESTOQUE: EstoqueRepository,
        }

    def create(self, repo_type: RepositoryType, **kwargs) -> BaseRepositoryInterface:
        """
        Cria instância do repositório especificado

        Args:
            repo_type: Tipo do repositório
            **kwargs: Argumentos adicionais (não utilizados nesta implementação)

        Returns:
            Instância do repositório configurado

        Raises:
            ConfigurationError: Se o tipo não for suportado
        """
        if not self.is_supported(repo_type):
            raise ConfigurationError(
                repo_type.value, f"Tipo de repositório não suportado: {repo_type.value}"
            )

        repository_class = self._repository_registry[repo_type]

        try:
            # Criar instância passando configuração do banco
            return repository_class(self.db_config.get_connection_dict())  # type: ignore[call-arg]

        except Exception as e:
            raise ConfigurationError(
                repo_type.value,
                f"Erro ao criar repositório {repo_type.value}: {str(e)}",
            )

    def is_supported(self, repo_type: RepositoryType) -> bool:
        """Verifica se o repositório é suportado"""
        return repo_type in self._repository_registry

    def get_supported_types(self) -> list[RepositoryType]:
        """Retorna lista de tipos suportados"""
        return list(self._repository_registry.keys())


class RepositoryFactoryManager:
    """
    Gerenciador de factories de repositório
    Permite diferentes implementações (PostgreSQL, MySQL, etc.)
    """

    def __init__(self) -> None:
        self._factories: Dict[str, RepositoryFactoryInterface] = {}
        self._default_factory: Optional[str] = None

    def register_factory(
        self,
        name: str,
        factory: RepositoryFactoryInterface,
        set_as_default: bool = False,
    ):
        """
        Registra uma factory

        Args:
            name: Nome da factory
            factory: Instância da factory
            set_as_default: Se deve definir como padrão
        """
        self._factories[name] = factory

        if set_as_default or self._default_factory is None:
            self._default_factory = name

    def create_repository(
        self, repo_type: RepositoryType, factory_name: Optional[str] = None, **kwargs
    ) -> BaseRepositoryInterface:
        """
        Cria repositório usando factory específica ou padrão

        Args:
            repo_type: Tipo do repositório
            factory_name: Nome da factory (opcional)
            **kwargs: Argumentos adicionais

        Returns:
            Instância do repositório

        Raises:
            ConfigurationError: Se factory não encontrada ou tipo não suportado
        """
        factory_to_use = factory_name or self._default_factory

        if not factory_to_use:
            raise ConfigurationError("factory", "Nenhuma factory registrada")

        if factory_to_use not in self._factories:
            raise ConfigurationError(
                factory_to_use, f"Factory não encontrada: {factory_to_use}"
            )

        factory = self._factories[factory_to_use]

        if not factory.is_supported(repo_type):
            raise ConfigurationError(
                repo_type.value,
                f"Repositório {repo_type.value} não suportado pela factory {factory_to_use}",
            )

        return factory.create(repo_type, **kwargs)

    def get_available_factories(self) -> list[str]:
        """Retorna lista de factories disponíveis"""
        return list(self._factories.keys())

    def get_supported_repositories(
        self, factory_name: Optional[str] = None
    ) -> list[RepositoryType]:
        """
        Retorna repositórios suportados por uma factory

        Args:
            factory_name: Nome da factory (opcional, usa padrão)

        Returns:
            Lista de tipos de repositório suportados
        """
        factory_to_use = factory_name or self._default_factory

        if not factory_to_use or factory_to_use not in self._factories:
            return []

        factory = self._factories[factory_to_use]

        # Se a factory implementa get_supported_types, usa; senão testa todos
        if hasattr(factory, "get_supported_types"):
            return cast(List[RepositoryType], factory.get_supported_types())

        # Testa todos os tipos
        supported = []
        for repo_type in RepositoryType:
            if factory.is_supported(repo_type):
                supported.append(repo_type)

        return supported


# Instância global do gerenciador
repository_manager = RepositoryFactoryManager()


def configure_repository_factories(db_config: DatabaseConfig):
    """
    Configura as factories padrão do sistema

    Args:
        db_config: Configuração do banco de dados
    """
    # Registrar factory PostgreSQL como padrão
    postgres_factory = DatabaseRepositoryFactory(db_config)
    repository_manager.register_factory(
        "postgresql", postgres_factory, set_as_default=True
    )


# Funções de conveniência
def create_repository(repo_type: RepositoryType, **kwargs) -> BaseRepositoryInterface:
    """Função de conveniência para criar repositórios"""
    return repository_manager.create_repository(repo_type, **kwargs)


def get_supported_repositories() -> list[RepositoryType]:
    """Função de conveniência para obter repositórios suportados"""
    return repository_manager.get_supported_repositories()
