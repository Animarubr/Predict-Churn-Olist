import pandas as pd
from config import DataBase
import os

PREDICT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELING_DIR = os.path.dirname(PREDICT_DIR)
BASE_DIR = os.path.dirname(MODELING_DIR)
MODELS_DIR = os.path.join(BASE_DIR, "models")

SRC_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = os.path.join(SRC_DIR, '.env')

model = pd.read_pickle(os.path.join(MODELS_DIR, "model_churn.pkl"))

db = DataBase()
con = db.connect_db("olist", ENV_DIR)
query_real_time = """SELECT * FROM olist.tb_book_sellers
                     WHERE seller_id = '{seller_id}'
                     AND dt_ref = (SELECT MAX(dt_ref) FROM olist.tb_book_sellers)          
                  """

def churn_score(seller_id):
    """Consome de uma tabela ja 'escorada'"""
    df = pd.read_sql_query(f"SELECT score FROM olist.tb_churn_score WHERE seller_id = '{seller_id}'", con)
    return df['score'][0]


def churn_real_time(seller_id):
    """'Escora' em tempo real"""
    df = pd.read_sql_query(query_real_time.format(seller_id=seller_id), con)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df_onehot = pd.DataFrame(model['onehot'].transform(df[model["cat_features"]]),
                            columns=model["onehot"].get_feature_names_out(model['cat_features']) 
                        )
    df_full = pd.concat([df[model["num_features"]], df_onehot],
                        axis=1)[model["features_fit"]]
    
    resp = model['model'].predict_proba(df_full)[:,1]
   
    return list(resp)
    