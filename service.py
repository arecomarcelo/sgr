# # service.py
# from django.contrib.auth.hashers import check_password
# from repository import UserRepository, DatabaseRepository

# class DataService:
#     def __init__(self):
#         # Configurações do banco de dados
#         self.DB_CONFIG = {
#             'dbname': 'sga',
#             'user': 'postgres',
#             'password': 'Zyxelpar100448',
#             'host': '195.200.1.244',
#             'port': '5432'
#         }
#         # Inicializar o repositório com as configurações do banco de dados
#         self.repository = DatabaseRepository(self.DB_CONFIG)

#     def get_data(self, table_name, campos):
#         # Passar campos como uma lista diretamente
#         return self.repository.fetch_data(table_name, campos)


# class UserService:
#     def __init__(self, data_service):
#         # Inicializar UserRepository com o DataService
#         self.user_repository = UserRepository(data_service.DB_CONFIG)

#     def validate_user(self, username, password):
#         user = self.user_repository.get_user(username)
#         if user and check_password(password, user[1]):
#             return True
#         return False



# service.py
from django.contrib.auth.hashers import check_password
from repository import UserRepository, DatabaseRepository

class DataService:
    def __init__(self):
        # Configurações do banco de dados
        self.DB_CONFIG = {
            'dbname': 'sga',
            'user': 'postgres',
            'password': 'Zyxelpar100448',
            'host': '195.200.1.244',
            'port': '5432'
        }
        # Inicializar o repositório com as configurações do banco de dados
        self.repository = DatabaseRepository(self.DB_CONFIG)

    def get_data(self, table_name, campos):
        # Passar campos como uma lista diretamente
        return self.repository.fetch_data(table_name, campos)


class UserService:
    def __init__(self, data_service):
        # Inicializar UserRepository com o DataService
        self.user_repository = UserRepository(data_service.DB_CONFIG)

    def validate_user(self, username, password):
        user = self.user_repository.get_user(username)
        if user and check_password(password, user[1]):
            # Se o usuário for válido, buscar permissões
            permissions = self.user_repository.get_user_permissions(user[0])  # user[0] é o ID do usuário
            return True, permissions
        return False, []
