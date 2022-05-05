import sqlalchemy
import dotenv
import os

class DataBase:
    
    def connect_db(self,schema_name, dotenv_path):
        dotenv.load_dotenv(dotenv_path)
        host = os.getenv(f'HOST_{schema_name.upper()}')
        port = os.getenv(f'PORT_{schema_name.upper()}')
        user = os.getenv(f'USER_{schema_name.upper()}')
        pswd = os.getenv(f'PSWD_{schema_name.upper()}')
        schema = os.getenv(f'SCHEMA_{schema_name.upper()}')

        str_connection = f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{schema}"
        return sqlalchemy.create_engine(str_connection)



class PrintLogs:
    
     def print_log(self, string):
        return print(f"{string}", end="")