import pandas as pd
from config import DataBase
import argparse
import os
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--dt_ref", help="Data referencia para a safra a ser predita: YYYY-MM-DD")
args = parser.parse_args()

PREDICT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELING_DIR = os.path.dirname(PREDICT_DIR)
BASE_DIR = os.path.dirname(MODELING_DIR)
MODELS_DIR = os.path.join(BASE_DIR, "models")

SRC_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = os.path.join(SRC_DIR, '.env')

print("Importando modelo..", end="")
model = pd.read_pickle(os.path.join(MODELS_DIR, "model_churn.pkl"))
print("Ok")

print("Abrindo conexão com o banco...", end="")
db = DataBase()
con = db.connect_db("olist", ENV_DIR)
print("Ok.")

print("Importando dados...", end="")
df = pd.read_sql_query(f"SELECT * FROM olist.tb_book_sellers WHERE dt_ref = '{args.dt_ref}';", con)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
print("Ok.")

print("Preparando dados para aplicar no modelo", end="")
df_onehot = pd.DataFrame(model['onehot'].transform(df[model["cat_features"]]),
                            columns=model["onehot"].get_feature_names_out(model['cat_features']) 
                        )
df_full = pd.concat([df[model["num_features"]], df_onehot], axis=1)[model["features_fit"]]

print("Ok.")

print("Criando score...", end="")
df["score"] = model["model"].predict_proba(df_full)[:,1]
print("Ok.")

print("Enviando os dados para o banco de dados...", end="")
df_score =  df[["dt_ref","seller_id", "score"]].copy()
df_score["dt_atualizacao"] = datetime.datetime.now()

df_score.to_sql("tb_churn_score", con, index=False, if_exists='replace', schema="olist")
print("Ok.")
