"""
Container de Injeção de Dependência simplificado para Vendas
Gerencia a criação e configuração das dependências da aplicação
"""
import logging
from typing import Any, Dict

from config.settings import Settings
from domain.services.vendas_service import VendasService
from infrastructure.database.repositories_vendas import (
    VendaAtualizacaoRepository,
    VendaPagamentoRepository,
    VendaProdutosRepository,
    VendaRepository,
)


class DIContainer:
    """Container de Injeção de Dependência simplificado"""

    def __init__(self):
        self.settings = Settings()
        self.logger = self._setup_logger()
        self._services: Dict[str, Any] = {}

    def _setup_logger(self) -> logging.Logger:
        """Configura logger"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def get_vendas_service(self) -> VendasService:
        """Obtém serviço de vendas com todas as dependências"""
        if "vendas_service" not in self._services:
            # Criar repositórios
            venda_repo = VendaRepository()
            pagamento_repo = VendaPagamentoRepository()
            produtos_repo = VendaProdutosRepository()
            atualizacao_repo = VendaAtualizacaoRepository()

            # Criar serviço com dependências injetadas
            self._services["vendas_service"] = VendasService(
                venda_repository=venda_repo,
                pagamento_repository=pagamento_repo,
                produtos_repository=produtos_repo,
                atualizacao_repository=atualizacao_repo,
            )

            self.logger.info("VendasService criado com sucesso")

        return self._services["vendas_service"]

    def clear_cache(self):
        """Limpa cache de serviços"""
        self._services.clear()
        self.logger.info("Container cache cleared")

    def health_check(self) -> Dict[str, bool]:
        """Verifica saúde dos serviços"""
        health = {}

        try:
            # Testar repositório de vendas
            venda_repo = VendaRepository()
            health["vendas"] = venda_repo.health_check()
        except Exception as e:
            health["vendas"] = False
            self.logger.error(f"Vendas health check failed: {e}")

        try:
            # Testar repositório de pagamentos
            pagamento_repo = VendaPagamentoRepository()
            health["pagamentos"] = pagamento_repo.health_check()
        except Exception as e:
            health["pagamentos"] = False
            self.logger.error(f"Pagamentos health check failed: {e}")

        try:
            # Testar repositório de produtos
            produtos_repo = VendaProdutosRepository()
            health["produtos"] = produtos_repo.health_check()
        except Exception as e:
            health["produtos"] = False
            self.logger.error(f"Produtos health check failed: {e}")

        try:
            # Testar repositório de atualizações
            atualizacao_repo = VendaAtualizacaoRepository()
            health["atualizacoes"] = atualizacao_repo.health_check()
        except Exception as e:
            health["atualizacoes"] = False
            self.logger.error(f"Atualizacoes health check failed: {e}")

        return health
