from django.contrib.auth.hashers import check_password

import pandas as pd

from repository import (
    BoletoRepository,
    ClienteRepository,
    DatabaseRepository,
    ExtratoRepository,
    UserRepository,
)


class DataService:
    def __init__(self):
        # Configurações do banco de dados
        self.DB_CONFIG = {
            "dbname": "sga",
            "user": "postgres",
            "password": "Zyxelpar100448",
            "host": "195.200.1.244",
            "port": "5432",
        }
        # Inicializar o repositório com as configurações do banco de dados
        self.repository = DatabaseRepository(self.DB_CONFIG)
        self.extrato_service = ExtratoService(self)  # Instanciando ExtratoService
        self.boletos_service = BoletoService(self)  # Instanciando BoletosService

    def get_data(self, table_name, campos):
        # Passar campos como uma lista diretamente
        return self.repository.fetch_data(table_name, campos)

    def get_extratos_filtrados(
        self, data_inicial, data_final, empresas=None, centros_custo=None
    ):
        """
        Obtém extratos filtrados com base nas datas e outros parâmetros.
        """
        return self.extrato_service.get_extratos_filtrados(
            data_inicial, data_final, empresas, centros_custo
        )

    def get_boletos_filtrados(self, data_inicial, data_final):
        """
        Obtém boletos filtrados com base nas datas.
        """
        return self.boletos_service.get_boletos_filtrados(data_inicial, data_final)

    def get_clientes(self) -> pd.DataFrame:
        """Obtém todos os clientes"""
        repo = ClienteRepository(self.DB_CONFIG)
        return repo.get_clientes()


class UserService:
    def __init__(self, data_service):
        # Inicializar UserRepository com o DataService
        self.user_repository = UserRepository(data_service.DB_CONFIG)

    def validate_user(self, username, password):
        user = self.user_repository.get_user(username)
        if user and check_password(password, user[1]):
            # Se o usuário for válido, buscar permissões
            permissions = self.user_repository.get_user_permissions(
                user[0]
            )  # user[0] é o ID do usuário
            return True, permissions
        return False, []


class ExtratoService:
    def __init__(self, data_service):
        self.extrato_repository = ExtratoRepository(data_service.DB_CONFIG)

    def get_extratos_filtrados(
        self, data_inicial, data_final, empresas=None, centros_custo=None
    ):
        """
        Obtém extratos filtrados com base nas datas e outros parâmetros.
        """
        return self.extrato_repository.get_extratos_filtrados(
            data_inicial, data_final, empresas, centros_custo
        )


class BoletoService:
    def __init__(self, data_service):
        self.boleto_repository = BoletoRepository(data_service.DB_CONFIG)

    def get_boletos_filtrados(self, data_inicial, data_final):
        """
        Obtém Boletos filtrados com base nas datas.
        """
        return self.boleto_repository.get_boletos_filtrados(data_inicial, data_final)


class ClienteService:
    def __init__(self, data_service):
        self.cliente_repository = ClienteRepository(data_service.DB_CONFIG)

    def get_clientes(self):
        """
        Obtém todos os clientes.
        """
        return self.cliente_repository.get_clientes()
