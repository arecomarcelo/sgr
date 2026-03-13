"""
Configurações centralizadas da aplicação SGR
Implementa padrão Singleton para configurações globais
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados PostgreSQL"""

    host: str = "195.200.1.244"
    port: int = 5432
    database: str = "sga"
    username: str = "postgres"
    password: str = "Zyxelpar100448"

    def get_connection_dict(self) -> dict:
        """Retorna dicionário de configuração para conexão"""
        return {
            "host": self.host,
            "port": str(self.port),
            "dbname": self.database,
            "user": self.username,
            "password": self.password,
        }

    def get_connection_url(self) -> str:
        """Retorna URL de conexão SQLAlchemy"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class AppConfig:
    """Configurações gerais da aplicação"""

    debug: bool = False
    title: str = "SGR - Sistema de Gestão de Recursos"
    cache_ttl: int = 300
    log_level: str = "INFO"
    secret_key: str = (
        "django-insecure-hly@8g(n3j9f=n+)eb7k6=bidr-!(vej3u@vnd^tk$h^-lk+ot"
    )
    session_timeout: int = 3600


@dataclass
class CacheConfig:
    """Configurações de cache Redis"""

    host: str = "localhost"
    port: int = 6379
    db: int = 0


class Settings:
    """Classe Singleton para gerenciar todas as configurações"""

    _instance: Optional["Settings"] = None
    _initialized: bool = False
    database: DatabaseConfig
    app: AppConfig
    cache: CacheConfig

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.database = DatabaseConfig()
            self.app = AppConfig()
            self.cache = CacheConfig()
            self._initialized = True

    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return bool(self.app.debug)

    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return not self.app.debug


# Instância global das configurações
settings = Settings()
