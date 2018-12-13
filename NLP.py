import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pickle
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('bigData')\
  .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1/bills_database.bills_115')\
  .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1/bills_database.bills_115')\
  .getOrCreate()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

df = spark.read.format('com.mongodb.spark.sql.DefaultSource').load()
categories = df.rdd
categories = categories.map(lambda row: (row['main_subject'], len(row['subjects'])))
categories = categories.filter(lambda row: row[0] is not None)
categories = categories.reduceByKey(lambda x, y: x+y)
categories = categories.toDF().toPandas()

subjects = df.filter(df['main_subject'] != '').filter(df['summary'] != '').toPandas()

subjects_list = subjects.main_subject.tolist()
subjects_list = list(set(subjects_list))

subjects['summary'] = subjects['summary'].map(lambda text: clean_text(text))
categories = subjects['main_subject'].apply(lambda x: x).str.get_dummies()

subjects = pd.concat([subjects, categories], axis=1)

subjects_train, subjects_test = train_test_split(subjects, random_state=42,
test_size=0.30, shuffle=True)
tfidf = TfidfVectorizer(stop_words=stop_words, smooth_idf=False, sublinear_tf=False, norm=None, analyzer='word')

x_train = tfidf.fit_transform(subjects_train.summary)
x_test = tfidf.transform(subjects_test.summary)

y_train = subjects_train[subjects_train.columns[14:]]
y_test = subjects_test[subjects_test.columns[14:]]

multinomialNB=OneVsRestClassifier(MultinomialNB(fit_prior=True, class_prior=None))
accuracy_multinomialNB = pd.DataFrame(columns=['Subject', 'Accuracy'])

i=0
for subj in subjects_list:
  multinomialNB.fit(x_train, y_train[subj])
  prediction = multinomialNB.predict(x_test)
  accuracy = accuracy_score(y_test[subj], prediction)
  print('test accuray for {} is {}'.format(subj, accuracy))
  accuracy_multinomialNB.loc[i, 'Subject'] = subj
  accuracy_multinomialNB.loc[i, 'Accuracy'] = accuracy
  i=i+1

bills_subjects_trace = [go.Bar(x=accuracy_multinomialNB['Subject'], y=accuracy_multinomialNB['Accuracy'])]
layout = go.Layout(title='Bill Subjecy Classification Accuracy(Multinomial NB')
fig = go.Figure(data=bills_subjects_trace, layout=layout)
py.plot(fig)
