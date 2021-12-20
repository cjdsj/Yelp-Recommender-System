import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm


''' 1. Read data '''
review_data = pd.read_csv('sentiment.csv')
review_data = review_data.drop(columns=['Unnamed: 0'])
review_data = review_data.drop(columns=['compound'])

user = pd.read_csv('user_topics.csv', index_col=0)
business = pd.read_csv('business_topics.csv', index_col=0)
user_categories = pd.read_csv('user_categories.csv')
business_categories = pd.read_csv('business_categories.csv')


''' 2. Compute topics_similarity '''
review_data['topics_similarity'] = [0 for _ in range(review_data.shape[0])]
review_data.loc[:, 'topics_similarity'] = review_data.loc[:, 'topics_similarity'].astype('float64')

for i in tqdm(range(review_data.shape[0])):
    user_id, business_id = review_data.loc[i, 'user_id'], review_data.loc[i, 'business_id']
    u = user.loc[user_id, :].values.reshape(1, -1)
    b = business.loc[business_id, :].values.reshape(1, -1)
    res = cosine_similarity(u, b)[0][0]
    review_data.at[i, 'topics_similarity'] = res


''' 3. Compute categories_similarity'''
review_data['categories_similarity'] = [0 for _ in range(review_data.shape[0])]
review_data.loc[:, 'categories_similarity'] = review_data.loc[:, 'categories_similarity'].astype('float64')

for i in tqdm(range(review_data.shape[0])):
    user_id, business_id = review_data.loc[i, 'user_id'], review_data.loc[i, 'business_id']
    u = user_categories.loc[user_id, :].values.reshape(1, -1)
    b = business_categories.loc[business_id, :].values.reshape(1, -1)
    res = cosine_similarity(u, b)[0][0]
    review_data.at[i, 'categories_similarity'] = res


''' 4. Add review_count (from business) and average_stars (from user) '''
business_data = pd.read_csv('yelp_academic_dataset_business.csv')
business_data = business_data[['business_id', 'review_count']]
business_data = business_data.set_index('business_id')

for i in tqdm(range(review_data.shape[0])):
    business_id = review_data.loc[i, 'business_id']
    review_data.at[i, 'review_count'] = business_data.at[business_id, 'review_count']

user_data = pd.read_csv('yelp_academic_dataset_user.csv')
user_data = user_data[['user_id', 'average_stars']]
user_data = user_data.set_index('user_id')

for i in tqdm(range(review_data.shape[0])):
    user_id = review_data.loc[i, 'user_id']
    review_data.at[i, 'average_stars'] = user_data.at[user_id, 'average_stars']


''' 5. Save data '''
review_data.to_csv('final_matrix.csv')
