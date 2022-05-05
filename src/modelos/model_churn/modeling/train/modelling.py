import pandas as pd
import os
import sqlalchemy
import dotenv

from sklearn import tree
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import preprocessing
import matplotlib.pyplot as plt


TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MODELING_DIR = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(MODELING_DIR)

SRC_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = os.path.join(SRC_DIR, '.env')

MODEL_DIR = os.path.join(BASE_DIR, 'models')

def connect_db(schema_name, dotenv_path):
    dotenv.load_dotenv(dotenv_path)
    host = os.getenv(f'HOST_{schema_name.upper()}')
    port = os.getenv(f'PORT_{schema_name.upper()}')
    user = os.getenv(f'USER_{schema_name.upper()}')
    pswd = os.getenv(f'PSWD_{schema_name.upper()}')
    schema = os.getenv(f'SCHEMA_{schema_name.upper()}')

    str_connection = f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{schema}"
    return sqlalchemy.create_engine(str_connection)

con = connect_db('olist', ENV_DIR)

abt = pd.read_sql_query('select * from olist.tb_abt_churn', con)
abt = abt.dropna()

df_oot = abt[abt['dt_ref'] == abt['dt_ref'].max()].copy() # Filtrando base out of time
df_oot.reset_index(drop=True, inplace=True)

df_abt = abt[abt['dt_ref'] < abt['dt_ref'].max()].copy() # Filtrando base abt

# Modelagem
# Definindo variáveis
target = 'flag_churn'
to_remove = ['dt_ref', 'seller_city', 'seller_id', target]

features = df_abt.columns.tolist()
for f in to_remove:
    features.remove(f)

cat_features = df_abt[features].dtypes[df_abt[features].dtypes == "object"].index.tolist()
num_features = list(set(features) - set(cat_features))

# Separando entre treino e teste
X = df_abt[features] # matriz de features ou variáveis
y = df_abt[target] # vetor da resposta ou target

# Separa teino e validação
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=1992)

X_train.reset_index(drop=True, inplace=True)
X_test.reset_index(drop=True, inplace=True)

onehot = preprocessing.OneHotEncoder(sparse=False, handle_unknown='ignore')
onehot.fit(X_train[cat_features]) # Treinou o onehot
onehot_df = pd.DataFrame(onehot.transform(X_train[cat_features]),
                         columns=onehot.get_feature_names_out(cat_features)) # Retorna o dado transformado

df_train = pd.concat([X_train[num_features], onehot_df], axis=1)
features_fit = df_train.columns.tolist()

# Modelo
clf = tree.DecisionTreeClassifier(min_samples_leaf=100)
clf.fit(df_train[features_fit], y_train)

rf = ensemble.RandomForestClassifier(n_estimators=500, min_samples_leaf=75, n_jobs=-3)
rf.fit(df_train[features_fit], y_train)

# Importancia das variaveis
#print(pd.Series(clf.feature_importances_, index=df_train.columns).sort_values(ascending=False)[:10])

#Analise na base de treino
y_train_proba = clf.predict_proba(df_train) # Calvula a probabilidade
y_train_proba_rf = rf.predict_proba(df_train) # Calvula a probabilidade

# AUC -> AREA UNDER CURVE
roc_train = metrics.roc_curve(y_train, y_train_proba[:,1])
auc_train = metrics.roc_auc_score(y_train, y_train_proba[:,1])

roc_train_rf = metrics.roc_curve(y_train, y_train_proba_rf[:,1])
auc_train_rf = metrics.roc_auc_score(y_train, y_train_proba_rf[:,1])

# print("ACC Base de Treino: ", auc_train)


#Analise na base de teste
onehot_df_test = pd.DataFrame(onehot.transform(X_test[cat_features]),
                              columns=onehot.get_feature_names_out(cat_features))
df_predict = pd.concat([X_test[num_features], onehot_df_test], axis=1)

y_test_proba = clf.predict_proba(df_predict)
y_test_proba_rf = rf.predict_proba(df_predict)

roc_test = metrics.roc_curve(y_test, y_test_proba[:,1])
auc_test = metrics.roc_auc_score(y_test, y_test_proba[:,1])

roc_test_rf = metrics.roc_curve(y_test, y_test_proba_rf[:,1])
auc_test_rf = metrics.roc_auc_score(y_test, y_test_proba_rf[:,1])

# print("ACC Base de Teste: ",acc_test)


#Analise na base out of time
onehot_df_oot = pd.DataFrame(onehot.transform(df_oot[cat_features]),
                              columns=onehot.get_feature_names_out(cat_features))

df_oot_predict = pd.concat([df_oot[num_features], onehot_df_oot], axis=1)

oot_proba = clf.predict_proba(df_oot_predict)
oot_proba_rf = rf.predict_proba(df_oot_predict)

roc_oot = metrics.roc_curve(df_oot[target], oot_proba[:,1])
auc_oot = metrics.roc_auc_score(y_test, y_test_proba[:,1])

roc_oot_rf = metrics.roc_curve(df_oot[target], oot_proba_rf[:,1])
auc_oot_rf = metrics.roc_auc_score(y_test, y_test_proba_rf[:,1])




#print("ACC Base Out of Time: ", acc_oot)

#fazendo o predict
abt.reset_index(drop=True, inplace=True)
df_abt_onehot = pd.DataFrame(onehot.transform(abt[cat_features]),
                             columns=onehot.get_feature_names_out(cat_features)
                            )

df_abt_predict = pd.concat([abt[num_features], df_abt_onehot], axis=1)

probs = clf.predict_proba(df_abt_predict)
abt["score_churn"] = clf.predict_proba(df_abt_predict)[:, 1]

abt_score = abt[['dt_ref','seller_id', "score_churn"]]
abt_score.to_sql('tb_churn_score', con, index=False, if_exists='replace', schema="olist")


# Plotando um grafico da curva roc
# plt.plot(roc_train[0], roc_train[1])
# plt.plot(roc_test[0], roc_test[1])
plt.plot(roc_oot[0], roc_oot[1])

# plt.plot(roc_train_rf[0], roc_train_rf[1])
# plt.plot(roc_test_rf[0], roc_test_rf[1])
plt.plot(roc_oot_rf[0], roc_oot_rf[1])

plt.xlabel("1 - Especificidade")
plt.ylabel("Sensibilidade")
plt.title("Curva ROC")
plt.legend([#f"Treino: {auc_train}",
            #f"Teste: {auc_test}",
            f"OOT Tree: {auc_oot}",
            #f"Treino RF: {auc_train_rf}",
            #f"Teste RF: {auc_test_rf}",
            f"OOT RF: {auc_oot_rf}"])
plt.show()


#salvando o modelo
model_data = pd.Series({
    "num_features": num_features,
    "cat_features": cat_features,
    "features_fit": features_fit,
    "model": rf,
    "onehot": onehot,
    "auc_train":auc_train_rf,
    "auc_test":auc_test_rf,
    "auc_oot":auc_oot_rf,
    "cutoff": 0.7
})

model_data.to_pickle(os.path.join(MODEL_DIR, "random_forest.pkl"))