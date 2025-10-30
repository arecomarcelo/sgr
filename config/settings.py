"""
Configurações centralizadas da aplicação SGR
Implementa padrão Singleton para configurações globais
"""

import os
from dataclasses import dataclass
from typing import Optional

from decouple import config


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados PostgreSQL"""

    host: str = config("DB_HOST", default="localhost")
    port: int = config("DB_PORT", default=5432, cast=int)
    database: str = config("DB_NAME", default="sga")
    username: str = config("DB_USER", default="postgres")
    password: str = config("DB_PASSWORD", default="")

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

    debug: bool = config("DEBUG", default=False, cast=bool)
    title: str = config("APP_TITLE", default="SGR - Sistema de Gestão de Recursos")
    cache_ttl: int = config("CACHE_TTL", default=300, cast=int)
    log_level: str = config("LOG_LEVEL", default="INFO")
    secret_key: str = config(
        "SECRET_KEY", default="development-key-change-in-production"
    )
    session_timeout: int = config("SESSION_TIMEOUT", default=3600, cast=int)


@dataclass
class CacheConfig:
    """Configurações de cache Redis"""

    host: str = config("REDIS_HOST", default="localhost")
    port: int = config("REDIS_PORT", default=6379, cast=int)
    db: int = config("REDIS_DB", default=0, cast=int)


class Settings:
    """Classe Singleton para gerenciar todas as configurações"""

    _instance: Optional["Settings"] = None
    _initialized: bool = False

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
        return self.app.debug

    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return not self.app.debug


# Instância global das configurações
settings = Settings()
