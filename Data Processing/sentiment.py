import numpy as np
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


''' 1. Read data '''
chunk_size = 1000000
csv_path = 'review.csv'
iter_data = pd.read_csv(csv_path, low_memory=False, chunksize=chunk_size)

for i, d in tqdm(enumerate(iter_data)):
    if i == 0:
        data = d
    else:
        data = pd.concat([data, d], axis=0)
# print(data.shape)


''' 2. Add sentiment information and save '''
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()
data['compound'] = data['text'].apply(lambda x:analyzer.polarity_scores(x)['compound'])
data = data.drop(['text'],axis=1)
data.to_csv('sentiment_only.csv')