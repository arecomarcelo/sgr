"""
Container de Injeção de Dependências para Recebimentos
"""

import logging
from typing import Optional

from domain.services.recebimentos_service import RecebimentosService
from infrastructure.database.repositories_recebimentos import RecebimentosRepository

logger = logging.getLogger(__name__)


class DIContainerRecebimentos:
    """Container de injeção de dependências para Recebimentos"""

    def __init__(self) -> None:
        self._recebimentos_repository: Optional[RecebimentosRepository] = None
        self._recebimentos_service: Optional[RecebimentosService] = None

    def get_recebimentos_repository(self) -> RecebimentosRepository:
        """Retorna instância do repositório de recebimentos"""
        if self._recebimentos_repository is None:
            self._recebimentos_repository = RecebimentosRepository()
            logger.info("✓ RecebimentosRepository inicializado")
        return self._recebimentos_repository

    def get_recebimentos_service(self) -> RecebimentosService:
        """Retorna instância do serviço de recebimentos"""
        if self._recebimentos_service is None:
            repository = self.get_recebimentos_repository()
            self._recebimentos_service = RecebimentosService(repository)
            logger.info("✓ RecebimentosService inicializado")
        return self._recebimentos_service

    def health_check(self) -> dict:
        """Verifica saúde dos serviços"""
        try:
            repository = self.get_recebimentos_repository()
            service = self.get_recebimentos_service()

            return {
                "repository": repository is not None,
                "service": service is not None,
            }
        except Exception as e:
            logger.error(f"Erro no health check: {str(e)}")
            return {
                "repository": False,
                "service": False,
            }
