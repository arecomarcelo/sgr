from typing import Any, Dict, List, Optional, Tuple, cast

import pandas as pd
import psycopg2
import psycopg2.extensions
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
            query = sql.SQL(
                """
                SELECT permission.codename 
                FROM auth_user_groups AS ug
                JOIN auth_group_permissions AS gp ON ug.group_id = gp.group_id
                JOIN auth_permission AS permission ON gp.permission_id = permission.id
                WHERE ug.user_id = %s
            """
            )
            cursor.execute(query, (user_id,))
            permissions = cursor.fetchall()
            return [
                perm[0] for perm in permissions
            ]  # Retornar apenas os nomes das permissões
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
            campos_formatados = ", ".join(
                [f'"{campo}"' for campo in campos]
            )  # Usar aspas duplas
            query = f'SELECT {campos_formatados} FROM "{table_name}";'
            return pd.read_sql(query, self.engine)
        except Exception as e:
            raise Exception(f"Erro ao buscar dados da tabela {table_name}: {e}")


class ExtratoRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def get_extratos_filtrados(
        self, data_inicial, data_final, empresas=None, centros_custo=None
    ):
        conn = self.connect()
        try:
            # data_inicial += ' 00:00:00'
            # data_final += ' 23:59:59'

            cursor = conn.cursor()
            query = sql.SQL(
                """
                SELECT b.descricao AS Banco, e.agencia, e.conta_corrente, e."data", 
                       e.documento, e.historico_descricao AS Descricao, e.valor, 
                       e.debito_credito AS "D/C", em.nome AS Empresa, 
                       cc.descricao AS CentroCusto
                FROM "Extratos" e 
                INNER JOIN "Bancos" b ON b.id = e.banco_id 
                LEFT JOIN "Empresas" em ON em.id = e.empresa_id
                LEFT JOIN "CentroCustos" cc ON cc.id = e.centrocusto_id
                WHERE e."data" BETWEEN %s AND %s
            """
            )

            params = [data_inicial, data_final]
            if empresas:
                query += sql.SQL(" AND em.nome IN %s")
                params.append(tuple(empresas))
            if centros_custo:
                query += sql.SQL(" AND cc.descricao IN %s")
                params.append(tuple(centros_custo))

            cursor.execute(query, params)
            extratos = cursor.fetchall()

            # Obter os nomes das colunas
            colunas = [desc[0] for desc in cursor.description]

            # Retornar um DataFrame
            return pd.DataFrame(extratos, columns=colunas)
        finally:
            cursor.close()
            conn.close()


class BoletoRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def get_boletos_filtrados(self, data_inicial, data_final):
        conn = self.connect()
        try:
            data_inicial += " 00:00:00"
            data_final += " 23:59:59"

            cursor = conn.cursor()
            query = sql.SQL(
                """
                select "Nome", "Boleto", "Vencimento", "DataHoraEnvio" as Envio, "Status" 
                from "BoletosEnviados"
                WHERE "DataHoraEnvio" BETWEEN %s AND %s                            
            """
            )

            params = [data_inicial, data_final]

            cursor.execute(query, params)
            extratos = cursor.fetchall()

            # Obter os nomes das colunas
            colunas = [desc[0] for desc in cursor.description]

            # Retornar um DataFrame
            return pd.DataFrame(extratos, columns=colunas)
        finally:
            cursor.close()
            conn.close()


class ClienteRepository:
    def __init__(self, db_config: Dict[str, Any]) -> None:
        self.db_config = db_config

    def connect(self) -> psycopg2.extensions.connection:
        """Establish database connection"""
        try:
            conn = cast(
                psycopg2.extensions.connection, psycopg2.connect(**self.db_config)
            )
            return conn
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def get_clientes(self) -> pd.DataFrame:
        """Get all client data"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT "TipoPessoa", 
                           COALESCE(NULLIF("RazaoSocial", ''), '-') AS "RazaoSocial", 
                           "Nome", "CNPJ", "CPF", "Email"
                    FROM "Clientes"
                    ORDER BY "RazaoSocial"
                """
                )
                clientes = cursor.fetchall()
                colunas = [desc[0] for desc in cursor.description]
                return pd.DataFrame(clientes, columns=colunas)
        finally:
            conn.close()
