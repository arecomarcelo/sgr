"""
Container de Injeção de Dependência simplificado para Vendas
Gerencia a criação e configuração das dependências da aplicação
"""

from typing import Any, Dict, cast

from config.settings import Settings
from core.logging_config import get_logger
from domain.services.vendas_service import VendasService
from infrastructure.database.repositories_vendas import (
    VendaAtualizacaoRepository,
    VendaPagamentoRepository,
    VendaProdutosRepository,
    VendaRepository,
)


class DIContainer:
    """Container de Injeção de Dependência simplificado"""

    def __init__(self) -> None:
        self.settings = Settings()
        self.logger = get_logger(__name__)
        self._services: Dict[str, Any] = {}
        self._service_creation_count: Dict[str, int] = {}  # Contador de criações

    def get_vendas_service(self) -> VendasService:
        """Obtém serviço de vendas com todas as dependências"""
        if "vendas_service" not in self._services:
            self.logger.debug("Inicializando VendasService com dependências...")

            try:
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

                # Incrementar contador e logar apenas na primeira vez
                self._service_creation_count["vendas"] = (
                    self._service_creation_count.get("vendas", 0) + 1
                )
                if self._service_creation_count["vendas"] == 1:
                    self.logger.info("✓ VendasService inicializado com 4 repositórios")
                else:
                    self.logger.debug(
                        f"VendasService reutilizado (criação #{self._service_creation_count['vendas']})"
                    )

            except Exception as e:
                self.logger.error(f"✗ Falha ao criar VendasService: {e}", exc_info=True)
                raise

        return cast(VendasService, self._services["vendas_service"])

    def clear_cache(self):
        """Limpa cache de serviços"""
        num_services = len(self._services)
        self._services.clear()
        if num_services > 0:
            self.logger.info(f"🗑 Cache limpo: {num_services} serviço(s) removido(s)")
        else:
            self.logger.debug("Cache já estava vazio")

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
