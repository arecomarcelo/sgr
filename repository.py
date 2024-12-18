# repository.py
import pandas as pd
from sqlalchemy import create_engine

class DatabaseRepository:
    def __init__(self, db_host, db_name, db_user, db_pass):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.engine = self.create_connection()

    def create_connection(self):
        try:
            engine = create_engine(f'postgresql://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}')
            return engine
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def fetch_data(self, table_name, campos):
        query = f'SELECT {campos} FROM {table_name};'
        return pd.read_sql(query, self.engine)