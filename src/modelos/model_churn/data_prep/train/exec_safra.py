import pandas as pd
import sqlalchemy
import os
import dotenv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", "-d", help="Data para referencia de safra. Formato YYYY-MM-DD", default="2017-04-01")

args = parser.parse_args()
date = args.date

# Caminhos raízes do projeto
MODELO_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(MODELO_DIR))))
BASE_DIR = os.path.dirname(SRC_DIR)
QUERY_DIR = os.path.join(SRC_DIR, 'queries')

# Informações para a conexão ao banco de dados
POSTGRES_SCHEMA = "olist"
ENV_DIR = os.path.join(SRC_DIR, '.env')

def import_query(path, **kwards):
    with open(path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result


def connect_db(schema_name, dotenv_path):
    dotenv.load_dotenv(dotenv_path)
    host = os.getenv(f'HOST_{schema_name.upper()}')
    port = os.getenv(f'PORT_{schema_name.upper()}')
    user = os.getenv(f'USER_{schema_name.upper()}')
    pswd = os.getenv(f'PSWD_{schema_name.upper()}')
    schema = os.getenv(f'SCHEMA_{schema_name.upper()}')

    str_connection = f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{schema}"
    return sqlalchemy.create_engine(str_connection)


query = import_query(os.path.join(QUERY_DIR, 'query_1.sql'))
query = query.format(date=date)

con = connect_db('olist', ENV_DIR)


try:
    print("\nTentando deletar a tabela", end="")
    con.execute(f"delete from olist.tb_book_sellers where dt_ref = '{date}'")
except:
    print('\nTabela não encontrada', end="")


try:
    print("\ntentando criar tabela...", end="")
    base_query = f'create table olist.tb_book_sellers as \n {query}'
    con.execute(base_query)

except:
    print("\nInserindo dados na tabela...", end="")
    base_query = f'insert into olist.tb_book_sellers \n {query}'
    con.execute(base_query)
    