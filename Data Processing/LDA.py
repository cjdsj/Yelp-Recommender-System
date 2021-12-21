from pyspark import SparkConf, SparkContext,SQLContext  
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.feature import Word2Vec, CountVectorizer  
from pyspark.ml.clustering import LDA, LDAModel  
from pyspark.sql.functions import col, udf  
from pyspark.sql.types import IntegerType, ArrayType, StringType
import pyspark.sql.functions as f
import pylab as pl
import numpy as np
import pandas as pd
from tqdm import tqdm
import re
import nltk
from nltk.corpus import stopwords


''' 1. Read data '''
data = sqlContext.read.format("csv") \
   .options(header='true', inferschema='true') \
   .load("gs://final-project-bucket-39/Project/review.csv")


''' 2. Preprocessing '''
# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Get RDD
reviews = data.rdd.map(lambda x : x['text']).filter(lambda x: x is not None)

# Filtering
tokens = reviews                                                   \
    .map( lambda document: document.strip().lower())               \
    .map( lambda document: re.split(" ", document))                \
    .map( lambda word: [x for x in word if x.isalpha()])           \
    .map( lambda word: [x for x in word if len(x) > 3] )           \
    .map( lambda word: [x for x in word if x not in stop_words])   \
    .zipWithIndex()


''' 3. TF-IDF '''
# Convert to DataFrame
df_txts = sqlContext.createDataFrame(tokens, ["list_of_words", "index"])

# TF
cv = CountVectorizer(inputCol="list_of_words", outputCol="raw_features")
cvmodel = cv.fit(df_txts)
result_cv = cvmodel.transform(df_txts)

# IDF
idf = IDF(inputCol="raw_features", outputCol="features")
idfModel = idf.fit(result_cv)
result_tfidf = idfModel.transform(result_cv)


''' 4. LDA '''
lda = LDA(k=10, maxIter=20)
res = result_tfidf[['index','features']]
lda_model = lda.fit(res)
transformed = lda_model.transform(result_tfidf).select("topicDistribution")  
# transformed.show(3, truncate=False)


''' 5. Save data '''
transformed_pd = transformed.toPandas()
transformed_pd_values = transformed_pd.iloc[:, 0].values
n = transformed_pd_values.shape[0]

begin = 0
while begin < n:
    print(begin)
    for i in tqdm(range(begin, n)):
        row = transformed_pd_values[i]
        if i == begin:
            transformed_np = np.reshape(row, (1, 10))
        else:
            transformed_np = np.append(transformed_np, np.reshape(row, (1, 10)), axis=0)
            if (i + 1) % 10000 == 0:
                break
    with open('transformed_np/' + str(begin) + '.npy', 'wb') as f:
        np.save(f, transformed_np)
    begin = i + 1