"""
Container de Injeção de Dependências para SGR
Implementa padrão Dependency Injection Container para gerenciar dependências
"""
import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Type

from config.settings import settings
from core.exceptions import ConfigurationError


class DIContainer:
    """
    Container de Injeção de Dependências simples
    Gerencia criação e ciclo de vida dos objetos
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._bindings: Dict[Type, Type] = {}

    def register_singleton(
        self, service_type: Type, implementation: Type = None
    ) -> "DIContainer":
        """
        Registra um serviço como singleton

        Args:
            service_type: Tipo/Interface do serviço
            implementation: Implementação concreta (opcional)
        """
        impl = implementation or service_type
        key = self._get_service_key(service_type)

        if key not in self._singletons:
            self._singletons[key] = None
            self._bindings[service_type] = impl

        return self

    def register_transient(
        self, service_type: Type, implementation: Type = None
    ) -> "DIContainer":
        """
        Registra um serviço como transiente (nova instância a cada resolução)

        Args:
            service_type: Tipo/Interface do serviço
            implementation: Implementação concreta (opcional)
        """
        impl = implementation or service_type
        self._bindings[service_type] = impl
        return self

    def register_factory(self, service_type: Type, factory: Callable) -> "DIContainer":
        """
        Registra uma factory para criar instâncias

        Args:
            service_type: Tipo do serviço
            factory: Função factory
        """
        key = self._get_service_key(service_type)
        self._factories[key] = factory
        return self

    def register_instance(self, service_type: Type, instance: Any) -> "DIContainer":
        """
        Registra uma instância específica

        Args:
            service_type: Tipo do serviço
            instance: Instância já criada
        """
        key = self._get_service_key(service_type)
        self._services[key] = instance
        return self

    def resolve(self, service_type: Type) -> Any:
        """
        Resolve uma dependência

        Args:
            service_type: Tipo do serviço a ser resolvido

        Returns:
            Instância do serviço

        Raises:
            ConfigurationError: Se o serviço não estiver registrado
        """
        key = self._get_service_key(service_type)

        # Verificar se já existe uma instância registrada
        if key in self._services:
            return self._services[key]

        # Verificar se é um singleton já criado
        if key in self._singletons and self._singletons[key] is not None:
            return self._singletons[key]

        # Verificar se tem factory
        if key in self._factories:
            instance = self._factories[key]()
            if key in self._singletons:
                self._singletons[key] = instance
            return instance

        # Criar instância usando bindings
        if service_type in self._bindings:
            implementation = self._bindings[service_type]
            instance = self._create_instance(implementation)

            # Armazenar como singleton se necessário
            if key in self._singletons:
                self._singletons[key] = instance

            return instance

        raise ConfigurationError(
            service_type.__name__, f"Serviço não registrado: {service_type.__name__}"
        )

    def _create_instance(self, implementation: Type) -> Any:
        """Cria uma instância resolvendo suas dependências"""
        try:
            # Obter o construtor
            constructor = implementation.__init__
            sig = inspect.signature(constructor)

            # Resolver dependências do construtor
            kwargs = {}
            for param_name, param in sig.parameters.items():
                if param_name == "self":
                    continue

                if param.annotation != param.empty:
                    # Tentar resolver a dependência
                    try:
                        kwargs[param_name] = self.resolve(param.annotation)
                    except ConfigurationError:
                        # Se não conseguir resolver, verificar se tem valor padrão
                        if param.default == param.empty:
                            raise ConfigurationError(
                                param.annotation.__name__,
                                f"Não foi possível resolver dependência: {param.annotation.__name__}",
                            )

            return implementation(**kwargs)

        except Exception as e:
            raise ConfigurationError(
                implementation.__name__,
                f"Erro ao criar instância de {implementation.__name__}: {str(e)}",
            )

    def _get_service_key(self, service_type: Type) -> str:
        """Gera chave única para o serviço"""
        return f"{service_type.__module__}.{service_type.__name__}"


# Container global da aplicação
container = DIContainer()


def configure_container() -> DIContainer:
    """
    Configura o container com os serviços padrão da aplicação

    Returns:
        Container configurado
    """
    from domain.repositories.interfaces import (
        BoletoRepositoryInterface,
        ClienteRepositoryInterface,
        DatabaseRepositoryInterface,
        ExtratoRepositoryInterface,
        UserRepositoryInterface,
    )
    from domain.services.boleto_service import BoletoService, BoletoServiceInterface
    from domain.services.cliente_service import ClienteService, ClienteServiceInterface
    from domain.services.data_service import DataService, DataServiceInterface
    from domain.services.extrato_service import ExtratoService, ExtratoServiceInterface
    from domain.services.user_service import UserService, UserServiceInterface
    from infrastructure.database.repositories import (
        BoletoRepository,
        ClienteRepository,
        DatabaseRepository,
        ExtratoRepository,
        UserRepository,
    )

    # Configurações
    container.register_instance(type(settings), settings)

    # Repositórios como singletons
    container.register_singleton(DatabaseRepositoryInterface, DatabaseRepository)
    container.register_singleton(UserRepositoryInterface, UserRepository)
    container.register_singleton(ClienteRepositoryInterface, ClienteRepository)
    container.register_singleton(ExtratoRepositoryInterface, ExtratoRepository)
    container.register_singleton(BoletoRepositoryInterface, BoletoRepository)

    # Serviços como singletons
    container.register_singleton(DataServiceInterface, DataService)
    container.register_singleton(UserServiceInterface, UserService)
    container.register_singleton(ExtratoServiceInterface, ExtratoService)
    container.register_singleton(BoletoServiceInterface, BoletoService)
    container.register_singleton(ClienteServiceInterface, ClienteService)

    return container


# Decorator para injeção automática
def inject(func: Callable) -> Callable:
    """
    Decorator para injeção automática de dependências

    Usage:
        @inject
        def some_function(service: SomeServiceInterface):
            return service.do_something()
    """

    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        # Resolver dependências que não foram fornecidas
        for param_name, param in sig.parameters.items():
            if param_name not in kwargs and param.annotation != param.empty:
                try:
                    kwargs[param_name] = container.resolve(param.annotation)
                except ConfigurationError:
                    # Se não conseguir resolver e não tem valor padrão, deixar como está
                    if param.default == param.empty:
                        continue

        return func(*args, **kwargs)

    return wrapper
