"""
Sistema de exceções customizadas para SGR
Implementa hierarquia de exceções específicas do domínio
"""

from typing import Any, Dict, Optional


class SGRException(Exception):
    """
    Exceção base do sistema SGR
    Todas as exceções customizadas devem herdar desta classe
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Converte exceção para dicionário para logging estruturado"""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class DatabaseError(SGRException):
    """Exceções relacionadas ao banco de dados"""

    pass


class DatabaseConnectionError(DatabaseError):
    """Erro de conexão com o banco de dados"""

    def __init__(
        self, message: str = "Erro ao conectar com o banco de dados", **kwargs
    ):
        super().__init__(message, **kwargs)


class DatabaseQueryError(DatabaseError):
    """Erro na execução de query no banco de dados"""

    def __init__(
        self, query: str, message: str = "Erro na execução da query", **kwargs
    ):
        super().__init__(message, **kwargs)
        self.details["query"] = query


class ValidationError(SGRException):
    """Exceções de validação de dados"""

    def __init__(self, field: str, message: str, value: Any = None, **kwargs):
        super().__init__(message, **kwargs)
        self.details.update({"field": field, "value": value})


class BusinessLogicError(SGRException):
    """Exceções da lógica de negócio"""

    pass


class AuthenticationError(SGRException):
    """Exceções de autenticação"""

    pass


class AuthorizationError(SGRException):
    """Exceções de autorização"""

    pass


class ConfigurationError(SGRException):
    """Exceções de configuração"""

    def __init__(self, component: str, message: str, **kwargs):
        super().__init__(message, **kwargs)
        self.details["component"] = component


class DataNotFoundError(SGRException):
    """Exceção quando dados não são encontrados"""

    def __init__(self, resource: str, identifier: Any = None, **kwargs):
        message = f"Recurso '{resource}' não encontrado"
        if identifier:
            message += f" (ID: {identifier})"

        super().__init__(message, **kwargs)
        self.details.update({"resource": resource, "identifier": identifier})


class ValidationError(SGRException):
    """Exceções de validação de dados"""

    def __init__(self, field: str, message: str, value: Any = None, **kwargs):
        super().__init__(f"Erro de validação no campo '{field}': {message}", **kwargs)
        self.details.update(
            {"field": field, "invalid_value": value, "validation_message": message}
        )


class AuthenticationError(SGRException):
    """Exceções de autenticação"""

    def __init__(self, message: str = "Credenciais inválidas", **kwargs):
        super().__init__(message, **kwargs)


class AuthorizationError(SGRException):
    """Exceções de autorização"""

    def __init__(self, resource: str, message: str = "Acesso negado", **kwargs):
        super().__init__(f"Acesso negado ao recurso: {resource}", **kwargs)
        self.details["resource"] = resource


class BusinessRuleError(SGRException):
    """Exceções de regras de negócio"""

    def __init__(self, rule: str, message: str, **kwargs):
        super().__init__(f"Violação da regra de negócio '{rule}': {message}", **kwargs)
        self.details["business_rule"] = rule


class DataNotFoundError(SGRException):
    """Exceções para dados não encontrados"""

    def __init__(self, entity: str, identifier: Any, **kwargs):
        super().__init__(f"{entity} não encontrado(a): {identifier}", **kwargs)
        self.details.update({"entity": entity, "identifier": identifier})


class ConfigurationError(SGRException):
    """Exceções de configuração"""

    def __init__(
        self, config_key: str, message: str = "Configuração inválida", **kwargs
    ):
        super().__init__(f"Erro de configuração '{config_key}': {message}", **kwargs)
        self.details["config_key"] = config_key


class ExternalServiceError(SGRException):
    """Exceções de serviços externos"""

    def __init__(
        self, service: str, message: str = "Erro no serviço externo", **kwargs
    ):
        super().__init__(f"Erro no serviço '{service}': {message}", **kwargs)
        self.details["service"] = service


class CacheError(SGRException):
    """Exceções relacionadas ao cache"""

    def __init__(self, operation: str, message: str = "Erro no cache", **kwargs):
        super().__init__(
            f"Erro na operação de cache '{operation}': {message}", **kwargs
        )
        self.details["cache_operation"] = operation
