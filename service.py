# service.py
from repository import DatabaseRepository

class DataService:
    def __init__(self):
        # Configurações do banco de dados
        self.DB_HOST = '195.200.1.244'  # Altere para o seu host
        self.DB_NAME = 'sga'  # Nome do banco de dados
        self.DB_USER = 'postgres'  # Usuário
        self.DB_PASS = 'Zyxelpar100448'  # Senha do usuário

        # Inicializar o repositório com as configurações do banco de dados
        self.repository = DatabaseRepository(self.DB_HOST, self.DB_NAME, self.DB_USER, self.DB_PASS)

    def get_data(self, table_name, campos):
        return self.repository.fetch_data(table_name, campos)