"""
Tratamento centralizado de erros para a aplicação SGR
Implementa decorators e handlers para captura e tratamento de exceções
"""
import functools
import logging
import traceback
from typing import Any, Callable, Optional

import streamlit as st

from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessRuleError,
    DatabaseError,
    DataNotFoundError,
    SGRException,
    ValidationError,
)

# Configure logger
logger = logging.getLogger(__name__)


def handle_errors(
    show_details: bool = False, fallback_message: str = "Ocorreu um erro inesperado"
):
    """
    Decorator para tratamento centralizado de erros

    Args:
        show_details: Se deve mostrar detalhes técnicos do erro
        fallback_message: Mensagem padrão para erros não tratados
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except SGRException as e:
                ErrorHandler.handle_sgr_exception(e, show_details)
                return None
            except Exception as e:
                ErrorHandler.handle_unexpected_exception(
                    e, fallback_message, show_details
                )
                return None

        return wrapper

    return decorator


class ErrorHandler:
    """Classe para centralizar o tratamento de erros"""

    @staticmethod
    def handle_sgr_exception(
        exception: SGRException, show_details: bool = False
    ) -> None:
        """Trata exceções customizadas do SGR"""

        # Log da exceção
        logger.warning(
            f"SGR Exception: {exception.error_code}",
            extra={
                "exception_type": type(exception).__name__,
                "message": exception.message,
                "details": exception.details,
            },
        )

        # Tratamento específico por tipo de exceção
        if isinstance(exception, ValidationError):
            st.error(f"🚫 **Erro de Validação**: {exception.message}")

        elif isinstance(exception, AuthenticationError):
            st.error("🔐 **Erro de Autenticação**: Credenciais inválidas")

        elif isinstance(exception, AuthorizationError):
            st.warning(
                "⚠️ **Acesso Negado**: Você não tem permissão para acessar este recurso"
            )

        elif isinstance(exception, BusinessRuleError):
            st.warning(f"📋 **Regra de Negócio**: {exception.message}")

        elif isinstance(exception, DataNotFoundError):
            st.info(f"📭 **Dados não encontrados**: {exception.message}")

        elif isinstance(exception, DatabaseError):
            st.error("🗄️ **Erro de Banco de Dados**: Problema na conexão ou consulta")

        else:
            st.error(f"❌ **Erro**: {exception.message}")

        # Mostrar detalhes se solicitado
        if show_details and exception.details:
            with st.expander("Detalhes técnicos"):
                st.json(exception.details)

    @staticmethod
    def handle_unexpected_exception(
        exception: Exception, fallback_message: str, show_details: bool = False
    ) -> None:
        """Trata exceções não customizadas"""

        # Log completo da exceção
        logger.error(
            "Unexpected exception occurred",
            exc_info=True,
            extra={
                "exception_type": type(exception).__name__,
                "message": str(exception),
            },
        )

        # Mostrar mensagem para o usuário
        st.error(f"❌ {fallback_message}")

        # Mostrar detalhes técnicos se solicitado
        if show_details:
            with st.expander("Detalhes técnicos"):
                st.code(traceback.format_exc())

    @staticmethod
    def show_success_message(message: str, icon: str = "✅") -> None:
        """Mostra mensagem de sucesso padronizada"""
        st.success(f"{icon} **{message}**")

    @staticmethod
    def show_info_message(message: str, icon: str = "ℹ️") -> None:
        """Mostra mensagem informativa padronizada"""
        st.info(f"{icon} {message}")

    @staticmethod
    def show_warning_message(message: str, icon: str = "⚠️") -> None:
        """Mostra mensagem de aviso padronizada"""
        st.warning(f"{icon} {message}")


# Decorator simplificado para uso comum
def safe_execute(func: Callable) -> Callable:
    """Decorator simplificado para execução segura"""
    return handle_errors(
        show_details=False, fallback_message="Operação não pôde ser concluída"
    )(func)


# Context manager para tratamento de erros
class ErrorContext:
    """Context manager para tratamento de erros em blocos específicos"""

    def __init__(self, operation_name: str, show_details: bool = False):
        self.operation_name = operation_name
        self.show_details = show_details

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if issubclass(exc_type, SGRException):
                ErrorHandler.handle_sgr_exception(exc_val, self.show_details)
            else:
                ErrorHandler.handle_unexpected_exception(
                    exc_val,
                    f"Erro na operação: {self.operation_name}",
                    self.show_details,
                )
        return True  # Suppress exception
