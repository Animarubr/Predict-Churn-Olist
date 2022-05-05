import sqlalchemy
import os
import dotenv

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PREP_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(DATA_PREP_DIR)

SRC_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = os.path.join(SRC_DIR, '.env')

def connect_db(schema_name, dotenv_path):
    dotenv.load_dotenv(dotenv_path)
    host = os.getenv(f'HOST_{schema_name.upper()}')
    port = os.getenv(f'PORT_{schema_name.upper()}')
    user = os.getenv(f'USER_{schema_name.upper()}')
    pswd = os.getenv(f'PSWD_{schema_name.upper()}')
    schema = os.getenv(f'SCHEMA_{schema_name.upper()}')

    str_connection = f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{schema}"
    return sqlalchemy.create_engine(str_connection)

def import_query(path, **kwards):
    with open(path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result

query = import_query(os.path.join(TRAIN_DIR, 'criacao_abt.sql'))
con = connect_db('olist', ENV_DIR)

for i in query.split(";")[:-1]:
    con.execute(i)