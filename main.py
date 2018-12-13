from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('bigData')\
  .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1/bills_database.bills_115')\
  .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1/bills_database.bills_115')\
  .getOrCreate()

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

df = spark.read.format('com.mongodb.spark.sql.DefaultSource').load()
bills_rdd = df.rdd
# subjects_count = df.map(lambda row: (row['subjects']))
# print the number of subjects related to a main subject
bills_subjects = bills_rdd.map(lambda row: (row['main_subject'], row['subjects']))
bills_subjects = bills_subjects.filter(lambda row: row[0] is not None)
bills_subjects = bills_subjects.reduceByKey(lambda x, y: list(set(x+y)))
bills_subjects = bills_subjects.map(lambda row: (row[0], len(row[1])))
bills_subjects = bills_subjects.toDF().orderBy(['_2'], ascending=[0,1]).toPandas()

bills_subjects_trace = [go.Bar(x=bills_subjects['_1'], y=bills_subjects['_2'])]
layout = go.Layout(title='Number of Bills per topic')
fig = go.Figure(data=bills_subjects_trace, layout=layout)
py.plot(fig)
def create_subject_enacted_comparison_graph():
  all_main_subject_count = df.groupBy('main_subject').count().orderBy(['count'], ascending=[0, 1])

  subject_count_pd = all_main_subject_count.select('main_subject', 'count').toPandas()
  subject_count_trace = go.Bar(x=subject_count_pd['main_subject'], y=subject_count_pd['count'], name='All Bills')

  enacted_subject_count = df.filter(df['enacted'] == True).groupby('main_subject').count().toPandas()
  enacted_trace = go.Bar(x=enacted_subject_count['main_subject'], y=enacted_subject_count['count'], name='Enacted Bills')

  data = [subject_count_trace, enacted_trace]
  layout = go.Layout(barmode='group', title='Bills Introduced vs Bills Enacted for 115th Congress')
  fig = go.Figure(data=data, layout=layout)
  py.plot(fig)
