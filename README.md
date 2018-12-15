# big_data_project_v2
Multinomial Niave Bayes Text Classification

Graphs can be found at https://plot.ly/organize/home/

Made with Pyspark

# Requirments:
Python 3.6.5
Pyspark >2
Plotly @latest
Numpy @latest
Pandas @latest
Scikit learn
Nltk @latest
pymongo @latest

# To reproduce
To reproduce the graphs you will need a plotly account

* You must be running a mongod session for the data to import correctly
* unzip the archives.zip
* once the requirements are fullfiled you can run the following commands in order

run:
* python utils.py 
* spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1 main.py
* spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1 NLP.py
