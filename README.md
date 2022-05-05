# Treinamento de Machine Learning do Canal Téo Me Why

## Este Repositório contém os estudos de Machine Learning da <a href="https://www.youtube.com/watch?v=TNDiiVwQ5Vo&list=PLvlkVRRKOYFQOK176fl9bLjzFkvhIOSwu">Playlist</a> do canal de Youtube do Téo Calvo.

<p>Este projeto visa criar um modelo de machine learning para prever o "churn" de vendedores, usando os dados da empresa de e-commerce brasileira Olist,
os dados podem ser encontrados no <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">Kaggle</a>,
os dados foram transformados de .csv para tabelas de um banco de dados relacional, no treinamento do Téo foi usado um banco SQLite, porém optei por usar o PostgresSQL como banco principal, então alguns comandos de sql contidos neste repositório podem diferir do treinamento.</p>

## Para realizar os comandos no terminal, foi criado um ambiente anaconda
#### Criando Conda Envirement
> conda create --name <envirement_name>
#### Ativando Envirement
> conda actvate <envirement-name>
*Em alguns casos para ativar o enviroment é preciso usar este comando:*
> source activate <envirement-name>

<p>
    A maior parte da limpesa e preparação dos dados foi feita usando etl.
</p>