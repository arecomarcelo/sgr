"""
Componentes de formulários reutilizáveis para SGR
Implementa padrão Component para elementos de formulário
"""

from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

import streamlit as st

from core.error_handler import ErrorHandler, handle_errors
from core.exceptions import ValidationError
from domain.validators import (
    DateRangeFilter,
    FiltroBoleto,
    FiltroExtrato,
    UserCredentials,
)


class FormComponent(ABC):
    """Interface base para componentes de formulário"""

    @abstractmethod
    def render(self) -> Dict[str, Any]:
        """
        Renderiza o componente de formulário

        Returns:
            Dados do formulário
        """
        pass

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Valida os dados do formulário

        Args:
            data: Dados a serem validados

        Returns:
            True se dados são válidos
        """
        pass


class DateRangeForm(FormComponent):
    """
    Componente de formulário para seleção de intervalo de datas
    Reutilizável em diferentes contextos
    """

    def __init__(
        self,
        title: str = "Período",
        default_days_back: int = 30,
        max_days_range: int = 365,
        show_time: bool = False,
        key_prefix: str = "date_range",
    ):
        self.title = title
        self.default_days_back = default_days_back
        self.max_days_range = max_days_range
        self.show_time = show_time
        self.key_prefix = key_prefix

        # Callbacks
        self._on_change: Optional[Callable[[Dict[str, Any]], None]] = None
        self._validation_callback: Optional[Callable[[Dict[str, Any]], bool]] = None

    def set_change_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Define callback para mudanças no formulário"""
        self._on_change = callback
        return self

    def set_validation_callback(self, callback: Callable[[Dict[str, Any]], bool]):
        """Define callback personalizado de validação"""
        self._validation_callback = callback
        return self

    @handle_errors(show_details=False)
    def render(self) -> Dict[str, Any]:
        """Renderiza o formulário de intervalo de datas"""
        st.subheader(f"📅 {self.title}")

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Data Inicial",
                value=date.today() - pd.Timedelta(days=self.default_days_back),
                key=f"{self.key_prefix}_start",
            )

        with col2:
            end_date = st.date_input(
                "Data Final", value=date.today(), key=f"{self.key_prefix}_end"
            )

        data = {"start_date": start_date, "end_date": end_date}

        # Validação em tempo real
        try:
            if self.validate(data):
                # Executar callback se definido
                if self._on_change:
                    self._on_change(data)

                return data

        except ValidationError as e:
            st.error(f"🚫 {e.message}")
            return {}

        return data

    def validate(self, data: Dict[str, Any]) -> bool:
        """Valida intervalo de datas"""
        try:
            # Validação com Pydantic
            date_range = DateRangeFilter(
                start_date=data["start_date"], end_date=data["end_date"]
            )

            # Validação personalizada se definida
            if self._validation_callback:
                return self._validation_callback(data)

            return True

        except Exception as e:
            raise ValidationError("date_range", str(e), data)


class LoginForm(FormComponent):
    """Componente de formulário de login"""

    def __init__(
        self,
        title: str = "Login",
        show_remember: bool = False,
        key_prefix: str = "login",
    ):
        self.title = title
        self.show_remember = show_remember
        self.key_prefix = key_prefix

        # Callbacks
        self._on_login: Optional[Callable] = None
        self._on_forgot_password: Optional[Callable] = None

    def set_login_callback(self, callback: Callable[[Dict[str, Any]], bool]):
        """Define callback para tentativa de login"""
        self._on_login = callback
        return self

    def set_forgot_password_callback(self, callback: Callable[[], None]):
        """Define callback para esqueci senha"""
        self._on_forgot_password = callback
        return self

    @handle_errors(show_details=False)
    def render(self) -> Dict[str, Any]:
        """Renderiza formulário de login"""
        # Aplicar estilo customizado
        self._apply_login_styles()

        st.markdown(f"### 🔐 {self.title}")

        with st.form(f"{self.key_prefix}_form"):
            username = st.text_input(
                "Usuário",
                placeholder="Digite seu nome de usuário",
                key=f"{self.key_prefix}_username",
            )

            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                key=f"{self.key_prefix}_password",
            )

            col1, col2 = st.columns([1, 1])

            with col1:
                login_button = st.form_submit_button(
                    "🚀 Entrar", use_container_width=True
                )

            with col2:
                if self.show_remember:
                    remember_me = st.checkbox("Lembrar-me")

            # Link esqueci senha
            if self._on_forgot_password:
                if st.form_submit_button("🔄 Esqueci minha senha"):
                    self._on_forgot_password()

        if login_button:
            data = {
                "username": username,
                "password": password,
                "remember_me": remember_me if self.show_remember else False,
            }

            if self.validate(data):
                if self._on_login:
                    success = self._on_login(data)
                    if success:
                        ErrorHandler.show_success_message(
                            "Login realizado com sucesso!"
                        )
                        st.rerun()
                    else:
                        st.error("🚫 Credenciais inválidas")

                return data

        return {}

    def validate(self, data: Dict[str, Any]) -> bool:
        """Valida dados de login"""
        try:
            credentials = UserCredentials(
                username=data["username"], password=data["password"]
            )
            return True

        except Exception as e:
            st.error(f"🚫 Erro de validação: {str(e)}")
            return False

    def _apply_login_styles(self):
        """Aplica estilos CSS para o formulário de login"""
        st.markdown(
            """
        <style>
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #1e88e5, #1976d2);
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: 600;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #1976d2, #1565c0);
            transform: translateY(-2px);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )


class FilterForm(FormComponent):
    """
    Componente genérico de formulário de filtros
    Configurável para diferentes tipos de filtros
    """

    def __init__(self, title: str = "Filtros", key_prefix: str = "filter"):
        self.title = title
        self.key_prefix = key_prefix
        self._fields: List[Dict[str, Any]] = []
        self._on_apply: Optional[Callable] = None

    def add_text_field(
        self, name: str, label: str, placeholder: str = "", default_value: str = ""
    ):
        """Adiciona campo de texto"""
        self._fields.append(
            {
                "type": "text",
                "name": name,
                "label": label,
                "placeholder": placeholder,
                "default": default_value,
            }
        )
        return self

    def add_select_field(
        self,
        name: str,
        label: str,
        options: List[str],
        default_index: int = 0,
        allow_multiple: bool = False,
    ):
        """Adiciona campo de seleção"""
        self._fields.append(
            {
                "type": "select",
                "name": name,
                "label": label,
                "options": options,
                "default_index": default_index,
                "multiple": allow_multiple,
            }
        )
        return self

    def add_number_field(
        self,
        name: str,
        label: str,
        min_value: float = None,
        max_value: float = None,
        default_value: float = 0.0,
        step: float = 1.0,
    ):
        """Adiciona campo numérico"""
        self._fields.append(
            {
                "type": "number",
                "name": name,
                "label": label,
                "min_value": min_value,
                "max_value": max_value,
                "default": default_value,
                "step": step,
            }
        )
        return self

    def add_date_field(self, name: str, label: str, default_value: date = None):
        """Adiciona campo de data"""
        self._fields.append(
            {
                "type": "date",
                "name": name,
                "label": label,
                "default": default_value or date.today(),
            }
        )
        return self

    def set_apply_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Define callback para aplicar filtros"""
        self._on_apply = callback
        return self

    @handle_errors(show_details=False)
    def render(self) -> Dict[str, Any]:
        """Renderiza formulário de filtros"""
        if not self._fields:
            st.warning("⚠️ Nenhum campo de filtro configurado")
            return {}

        st.subheader(f"🔍 {self.title}")

        data = {}

        # Calcular número de colunas (máximo 3)
        cols = st.columns(min(len(self._fields), 3))

        for idx, field in enumerate(self._fields):
            col_idx = idx % len(cols)

            with cols[col_idx]:
                value = self._render_field(field)
                data[field["name"]] = value

        # Botões de ação
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("🔍 Aplicar Filtros", key=f"{self.key_prefix}_apply"):
                if self.validate(data):
                    if self._on_apply:
                        self._on_apply(data)
                    return data

        with col2:
            if st.button("🔄 Limpar", key=f"{self.key_prefix}_clear"):
                st.rerun()

        return data

    def _render_field(self, field: Dict[str, Any]) -> Any:
        """Renderiza um campo específico"""
        field_type = field["type"]
        name = field["name"]
        label = field["label"]

        key = f"{self.key_prefix}_{name}"

        if field_type == "text":
            return st.text_input(
                label,
                value=field["default"],
                placeholder=field.get("placeholder", ""),
                key=key,
            )

        elif field_type == "select":
            if field.get("multiple", False):
                return st.multiselect(label, options=field["options"], key=key)
            else:
                return st.selectbox(
                    label,
                    options=field["options"],
                    index=field.get("default_index", 0),
                    key=key,
                )

        elif field_type == "number":
            return st.number_input(
                label,
                min_value=field.get("min_value"),
                max_value=field.get("max_value"),
                value=field["default"],
                step=field.get("step", 1.0),
                key=key,
            )

        elif field_type == "date":
            return st.date_input(label, value=field["default"], key=key)

        return None

    def validate(self, data: Dict[str, Any]) -> bool:
        """Validação básica do formulário"""
        # Implementar validações específicas conforme necessário
        return True


import pandas as pd

# Classes especializadas para filtros específicos


class ExtratoFilterForm(DateRangeForm):
    """Formulário especializado para filtros de extrato"""

    def __init__(self, **kwargs):
        super().__init__(title="Filtrar Extratos", **kwargs)
        self.companies = []
        self.cost_centers = []

    def set_options(self, companies: List[str], cost_centers: List[str]):
        """Define opções de empresas e centros de custo"""
        self.companies = companies
        self.cost_centers = cost_centers
        return self

    def render(self) -> Dict[str, Any]:
        """Renderiza formulário com filtros específicos de extrato"""
        # Renderizar seleção de datas
        date_data = super().render()

        if not date_data:
            return {}

        # Adicionar filtros específicos
        col1, col2 = st.columns(2)

        with col1:
            selected_companies = st.multiselect(
                "Empresas", options=self.companies, key=f"{self.key_prefix}_companies"
            )

        with col2:
            selected_cost_centers = st.multiselect(
                "Centros de Custo",
                options=self.cost_centers,
                key=f"{self.key_prefix}_cost_centers",
            )

        # Combinar dados
        data = {
            **date_data,
            "empresas": selected_companies if selected_companies else None,
            "centros_custo": selected_cost_centers if selected_cost_centers else None,
        }

        return data

    def validate(self, data: Dict[str, Any]) -> bool:
        """Validação específica para filtros de extrato"""
        try:
            filtro = FiltroExtrato(
                data_inicial=data["start_date"],
                data_final=data["end_date"],
                empresas=data.get("empresas"),
                centros_custo=data.get("centros_custo"),
            )
            return True
        except Exception as e:
            st.error(f"🚫 Erro na validação: {str(e)}")
            return False
