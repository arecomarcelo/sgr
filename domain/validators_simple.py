"""
Validadores simples para o domínio de vendas (sem Pydantic)
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional


@dataclass
class VendasFilterValidator:
    """Validador para filtros de vendas"""

    data_inicio: date
    data_fim: date
    vendedores: List[str]
    situacoes: List[str]

    def __post_init__(self):
        """Validação após inicialização"""
        self.validate()

    def validate(self):
        """Valida os dados"""
        if self.data_inicio > self.data_fim:
            raise ValueError("Data inicial não pode ser maior que data final")


@dataclass
class DateRangeValidator:
    """Validador para intervalos de datas"""

    start_date: date
    end_date: date

    def __post_init__(self):
        """Validação após inicialização"""
        self.validate()

    def validate(self):
        """Valida o intervalo de datas"""
        if self.start_date > self.end_date:
            raise ValueError("Data inicial não pode ser maior que data final")

        if self.start_date > date.today():
            raise ValueError("Data inicial não pode ser no futuro")


class SimpleValidator:
    """Validador simples para casos gerais"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return False

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """Valida intervalo de datas"""
        try:
            DateRangeValidator(start_date=start_date, end_date=end_date)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_required_field(value: Any, field_name: str) -> bool:
        """Valida campo obrigatório"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"Campo '{field_name}' é obrigatório")
        return True

    @staticmethod
    def validate_list_not_empty(items: List[Any], field_name: str) -> bool:
        """Valida que lista não está vazia"""
        if not items or len(items) == 0:
            raise ValueError(f"Lista '{field_name}' não pode estar vazia")
        return True
