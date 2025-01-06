# # repository.py
# import pandas as pd
# import psycopg2
# from psycopg2 import sql
# from sqlalchemy import create_engine

# class UserRepository:
#     def __init__(self, db_config):
#         self.db_config = db_config

#     def connect(self):
#         try:
#             conn = psycopg2.connect(**self.db_config)
#             return conn
#         except Exception as e:
#             raise Exception(f"Erro ao conectar ao banco de dados: {e}")

#     def get_user(self, username):
#         conn = self.connect()
#         try:
#             cursor = conn.cursor()
#             query = sql.SQL("SELECT * FROM auth_user WHERE username = %s")
#             cursor.execute(query, (username,))
#             user = cursor.fetchone()
#             return user
#         finally:
#             cursor.close()
#             conn.close()


# class DatabaseRepository:
#     def __init__(self, db_config):
#         self.db_config = db_config
#         self.engine = self.create_connection()

#     def create_connection(self):
#         try:
#             # Usando o SQLAlchemy para criar a engine
#             engine = create_engine(
#                 f'postgresql://{self.db_config["user"]}:{self.db_config["password"]}@'
#                 f'{self.db_config["host"]}/{self.db_config["dbname"]}'
#             )
#             return engine
#         except Exception as e:
#             raise Exception(f"Erro ao conectar ao banco de dados: {e}")

#     def fetch_data(self, table_name, campos):
#         try:
#             # Formatar os campos para a consulta SQL
#             campos_formatados = ', '.join([f'"{campo}"' for campo in campos])  # Usar aspas duplas
#             query = f'SELECT {campos_formatados} FROM "{table_name}";'
#             return pd.read_sql(query, self.engine)
#         except Exception as e:
#             raise Exception(f"Erro ao buscar dados da tabela {table_name}: {e}")




# repository.py
import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

class UserRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def get_user(self, username):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = sql.SQL("SELECT * FROM auth_user WHERE username = %s")
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            conn.close()

    def get_user_permissions(self, user_id):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = sql.SQL("""
                SELECT permission.codename 
                FROM auth_user_groups AS ug
                JOIN auth_group_permissions AS gp ON ug.group_id = gp.group_id
                JOIN auth_permission AS permission ON gp.permission_id = permission.id
                WHERE ug.user_id = %s
            """)
            cursor.execute(query, (user_id,))
            permissions = cursor.fetchall()
            return [perm[0] for perm in permissions]  # Retornar apenas os nomes das permissões
        finally:
            cursor.close()
            conn.close()


class DatabaseRepository:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = self.create_connection()

    def create_connection(self):
        try:
            # Usando o SQLAlchemy para criar a engine
            engine = create_engine(
                f'postgresql://{self.db_config["user"]}:{self.db_config["password"]}@'
                f'{self.db_config["host"]}/{self.db_config["dbname"]}'
            )
            return engine
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def fetch_data(self, table_name, campos):
        try:
            # Formatar os campos para a consulta SQL
            campos_formatados = ', '.join([f'"{campo}"' for campo in campos])  # Usar aspas duplas
            query = f'SELECT {campos_formatados} FROM "{table_name}";'
            return pd.read_sql(query, self.engine)
        except Exception as e:
            raise Exception(f"Erro ao buscar dados da tabela {table_name}: {e}")
