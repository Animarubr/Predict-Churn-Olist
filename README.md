# Treinamento de Machine Learning do Canal Téo Me Why

## Este Repositório contém os estudos de Machine Learning da <a href="https://www.youtube.com/watch?v=TNDiiVwQ5Vo&list=PLvlkVRRKOYFQOK176fl9bLjzFkvhIOSwu">Playlist</a> do canal de Youtube do <a href="https://www.youtube.com/channel/UC-Xa9J9-B4jBOoBNIHkMMKA">Téo Calvo</a>.

<p>Este projeto visa criar um modelo de machine learning para prever o "churn"|desistencia de vendedores, usando os dados da empresa de e-commerce brasileira Olist,
os dados podem ser encontrados no <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">Kaggle</a>,
os dados foram transformados de .csv para tabelas de um banco de dados relacional, no treinamento do Téo foi usado um banco SQLite, porém optei por usar o PostgresSQL como banco principal, então alguns comandos de sql contidos neste repositório podem diferir do treinamento.</p>

## Para realizar os comandos no terminal foi criado um ambiente anaconda
#### Criando Conda Environment
> conda create --name <environment_name>
#### Ativando Environment
> conda actvate <environment-name>
#### Em alguns casos para ativar o environment é preciso usar este comando
> source activate <environment-name>

<p>
    A maior parte da limpeza e preparação dos dados foi feita usando etl.
</p>