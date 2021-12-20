import numpy as np
import pandas as pd


''' 1. Read reviews data '''
chunk_size = 1000000
csv_path = 'yelp_academic_dataset_review.csv'
iter_data = pd.read_csv(csv_path, low_memory=False, chunksize=chunk_size)

for i, d in enumerate(iter_data):
    if i == 0:
        data = d
    else:
        data = pd.concat([data, d], axis=0)

reviews_data = data[['business_id', 'user_id', 'stars', 'text']]
# print(data.shape)


''' 2. Read business data '''
csv_path = 'business.csv'
business_data = pd.read_csv(csv_path, low_memory=False)
business_data = business_data.drop(columns=['Unnamed: 0'])


''' 3. Delete reviews given to businesses which are not restaurants '''
remain_bus = business_data.loc[:, 'business_id'].unique()
remain_bus = set(remain_bus.tolist())

drop_reviews = []
for i in range(reviews_data.shape[0]):
    if reviews_data.loc[i, 'business_id'] not in remain_bus:
        drop_reviews.append(i)

reviews_data.drop(index=drop_reviews, inplace=True)
reviews_data = reviews_data.reset_index(drop=True)


''' 4. Delete reviews given by inactivate users '''
user = data.loc[:, 'user_id']
count = user.value_counts()

threshold = 5
inactivate_users = set()
append_flag = False
i = 0
for i in range(count.shape[0]):
    if count[i] <= threshold:
        break
for j in range(i, count.shape[0]):
    inactivate_users.add(count.index[j])

drop_reviews = []
for i in range(reviews_data.shape[0]):
    if reviews_data.loc[i, 'user_id'] in inactivate_users:
        drop_reviews.append(i)

reviews_data.drop(index=drop_reviews, inplace=True)
reviews_data = reviews_data.reset_index(drop=True)
# print(reviews_data.shape)


''' 5. Process 'text' column for Spark '''
reviews_data = reviews_data.replace(r'\r', ' ', regex=True)
reviews_data = reviews_data.replace(r'\n', ' ', regex=True)

text = reviews_data.loc[:, ['text']]
for i in range(reviews_data.shape[0]):
    if type(text.loc[i, 'text']) != str:
        reviews_data.drop([i], inplace=True)


''' 6. Save data for csv file '''
reviews_data.to_csv('review.csv')
