"""
Sistema de validação usando Pydantic para SGR
Implementa modelos de validação para todas as entidades do sistema
"""
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, validator


class TipoPessoa(str, Enum):
    """Enum para tipo de pessoa"""

    FISICA = "PF"
    JURIDICA = "PJ"


class StatusBoleto(str, Enum):
    """Enum para status do boleto"""

    ENVIADO = "Enviado"
    PENDENTE = "Pendente"
    PAGO = "Pago"
    VENCIDO = "Vencido"


class DebitoCredito(str, Enum):
    """Enum para débito/crédito"""

    DEBITO = "D"
    CREDITO = "C"


# ================================
# VALIDADORES DE DADOS DE ENTRADA
# ================================


class DateRangeFilter(BaseModel):
    """Validador para filtros de intervalo de datas"""

    start_date: date = Field(..., description="Data inicial do filtro")
    end_date: date = Field(..., description="Data final do filtro")

    @validator("start_date")
    def validate_start_date(cls, v):
        if v > date.today():
            raise ValueError("Data inicial não pode ser no futuro")
        return v

    @validator("end_date")
    def validate_end_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("Data final deve ser posterior à data inicial")
        if v > date.today():
            raise ValueError("Data final não pode ser no futuro")
        return v

    @validator("end_date")
    def validate_date_range(cls, v, values):
        # Validação de 365 dias removida - período sem limite
        # Avisos de performance são exibidos na interface quando apropriado
        return v


class UserCredentials(BaseModel):
    """Validador para credenciais de usuário"""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Nome de usuário"
    )
    password: str = Field(..., min_length=6, description="Senha do usuário")

    @validator("username")
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError("Nome de usuário não pode estar vazio")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Nome de usuário deve conter apenas letras, números, _ e -"
            )
        return v.strip().lower()

    @validator("password")
    def validate_password(cls, v):
        if len(v.strip()) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        return v


class DatabaseQueryParams(BaseModel):
    """Validador para parâmetros de consulta ao banco"""

    table_name: str = Field(..., min_length=1, description="Nome da tabela")
    fields: List[str] = Field(
        ..., min_items=1, description="Campos a serem selecionados"
    )

    @validator("table_name")
    def validate_table_name(cls, v):
        # Validação básica contra SQL injection
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Nome da tabela contém caracteres inválidos")
        return v

    @validator("fields")
    def validate_fields(cls, v):
        if not v:
            raise ValueError("Pelo menos um campo deve ser especificado")

        # Validação básica dos nomes dos campos
        for field in v:
            if not isinstance(field, str) or not field.strip():
                raise ValueError(f"Nome de campo inválido: {field}")

            # Remover aspas duplas para validação
            clean_field = field.strip().replace('"', "")
            if not clean_field.replace("_", "").replace("-", "").isalnum():
                raise ValueError(f"Nome de campo contém caracteres inválidos: {field}")

        return v


# ================================
# MODELOS DE ENTIDADES
# ================================


class Cliente(BaseModel):
    """Modelo de validação para Cliente"""

    tipo_pessoa: TipoPessoa = Field(..., description="Tipo de pessoa (PF/PJ)")
    razao_social: Optional[str] = Field(
        None, max_length=200, description="Razão social (apenas PJ)"
    )
    nome: str = Field(..., min_length=2, max_length=200, description="Nome do cliente")
    cnpj: Optional[str] = Field(None, description="CNPJ (apenas PJ)")
    cpf: Optional[str] = Field(None, description="CPF (apenas PF)")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")

    @validator("razao_social")
    def validate_razao_social(cls, v, values):
        if "tipo_pessoa" in values:
            if values["tipo_pessoa"] == TipoPessoa.JURIDICA and not v:
                raise ValueError("Razão social é obrigatória para pessoa jurídica")
        return v

    @validator("cnpj")
    def validate_cnpj(cls, v, values):
        if "tipo_pessoa" in values:
            if values["tipo_pessoa"] == TipoPessoa.JURIDICA:
                if not v:
                    raise ValueError("CNPJ é obrigatório para pessoa jurídica")
                # Validação básica de formato CNPJ
                cnpj_numbers = "".join(filter(str.isdigit, v))
                if len(cnpj_numbers) != 14:
                    raise ValueError("CNPJ deve ter 14 dígitos")
            elif values["tipo_pessoa"] == TipoPessoa.FISICA and v:
                raise ValueError("CNPJ não deve ser informado para pessoa física")
        return v

    @validator("cpf")
    def validate_cpf(cls, v, values):
        if "tipo_pessoa" in values:
            if values["tipo_pessoa"] == TipoPessoa.FISICA:
                if not v:
                    raise ValueError("CPF é obrigatório para pessoa física")
                # Validação básica de formato CPF
                cpf_numbers = "".join(filter(str.isdigit, v))
                if len(cpf_numbers) != 11:
                    raise ValueError("CPF deve ter 11 dígitos")
            elif values["tipo_pessoa"] == TipoPessoa.JURIDICA and v:
                raise ValueError("CPF não deve ser informado para pessoa jurídica")
        return v


class Boleto(BaseModel):
    """Modelo de validação para Boleto"""

    nome: str = Field(..., min_length=2, max_length=200, description="Nome do cliente")
    boleto: str = Field(..., min_length=1, description="Identificador do boleto")
    vencimento: date = Field(..., description="Data de vencimento")
    data_hora_envio: datetime = Field(..., description="Data e hora do envio")
    status: StatusBoleto = Field(..., description="Status do boleto")

    @validator("vencimento")
    def validate_vencimento(cls, v):
        # Vencimento pode ser no passado ou futuro
        return v

    @validator("data_hora_envio")
    def validate_data_hora_envio(cls, v):
        if v > datetime.now():
            raise ValueError("Data de envio não pode ser no futuro")
        return v


class Extrato(BaseModel):
    """Modelo de validação para Extrato bancário"""

    banco: str = Field(..., min_length=1, max_length=100, description="Nome do banco")
    agencia: str = Field(..., min_length=1, max_length=20, description="Agência")
    conta_corrente: str = Field(
        ..., min_length=1, max_length=20, description="Conta corrente"
    )
    data: date = Field(..., description="Data da movimentação")
    documento: Optional[str] = Field(
        None, max_length=50, description="Número do documento"
    )
    descricao: str = Field(
        ..., min_length=1, max_length=500, description="Descrição da movimentação"
    )
    valor: float = Field(..., gt=0, description="Valor da movimentação")
    debito_credito: DebitoCredito = Field(..., description="Tipo de movimentação (D/C)")
    empresa: Optional[str] = Field(None, max_length=200, description="Nome da empresa")
    centro_custo: Optional[str] = Field(
        None, max_length=200, description="Centro de custo"
    )

    @validator("valor")
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError("Valor deve ser positivo")
        # Limitar a 2 casas decimais
        return round(v, 2)


class Produto(BaseModel):
    """Modelo de validação para Produto/Estoque"""

    codigo: Optional[str] = Field(None, max_length=50, description="Código do produto")
    descricao: str = Field(
        ..., min_length=1, max_length=500, description="Descrição do produto"
    )
    valor_custo: Optional[float] = Field(None, ge=0, description="Valor de custo")
    valor_venda: Optional[float] = Field(None, ge=0, description="Valor de venda")
    estoque_galpao: Optional[int] = Field(None, ge=0, description="Estoque no galpão")

    @validator("valor_venda")
    def validate_valor_venda(cls, v, values):
        if (
            v is not None
            and "valor_custo" in values
            and values["valor_custo"] is not None
        ):
            if v < values["valor_custo"]:
                raise ValueError(
                    "Valor de venda não pode ser menor que o valor de custo"
                )
        return v

    @validator("valor_custo", "valor_venda")
    def validate_valores(cls, v):
        if v is not None and v < 0:
            raise ValueError("Valores não podem ser negativos")
        return round(v, 2) if v is not None else v


# ================================
# VALIDADORES PARA FILTROS
# ================================


class FiltroExtrato(BaseModel):
    """Validador para filtros de extrato"""

    data_inicial: date
    data_final: date
    empresas: Optional[List[str]] = None
    centros_custo: Optional[List[str]] = None

    @validator("data_final")
    def validate_date_range(cls, v, values):
        if "data_inicial" in values and v < values["data_inicial"]:
            raise ValueError("Data final deve ser posterior à data inicial")
        return v


class FiltroBoleto(BaseModel):
    """Validador para filtros de boleto"""

    data_inicial: date
    data_final: date

    @validator("data_final")
    def validate_date_range(cls, v, values):
        if "data_inicial" in values and v < values["data_inicial"]:
            raise ValueError("Data final deve ser posterior à data inicial")
        return v
