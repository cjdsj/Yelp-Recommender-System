import numpy as np
import pandas as pd
import collections
from tqdm import tqdm


def categories_for_dict(s):
    global categories_dict
    if s is np.nan or s == 'None' or s == 'none':
        return np.nan
    features = s.split(sep=', ')
    for f in features:
        categories_dict[f] += 1


def categories_for_set(s):
    global categories_set
    res = []
    features = s.split(sep=', ')
    for f in features:
        if f in categories_set:
            res.append(f)
    return res


''' 1. Read data '''
review_data = pd.read_csv('sentiment.csv')
review_data = review_data.drop(columns=['Unnamed: 0'])
review_data = review_data.drop(columns=['compound'])

business_data = pd.read_csv('business.csv')
business_data = business_data.drop(columns=['Unnamed: 0'])


''' 2. Filter categories '''
categories_dict = collections.defaultdict(int)
business_data['categories'].apply(categories_for_dict)

categories_set = set()
for k, v in categories_dict.items():
    if 15000 > v > 20:
        categories_set.add(k)


''' 3. Delete unwanted categories '''
business_data = business_data[['business_id', 'categories']]
business_data['categories'] = business_data['categories'].apply(categories_for_set)


''' 4. Get users and businesses by reviews '''
business_name = review_data.loc[:, 'business_id'].unique()
business_name = business_name.tolist()

user_name = review_data.loc[:, 'user_id'].unique()
user_name = user_name.tolist()


''' 5. Get categories for business '''
categories_columns = list(categories_set)
categories_columns.sort()
n = len(categories_columns)
business_categories = pd.DataFrame(np.zeros((business_data.shape[0], n + 1)),
                                   columns=['business_id'] + categories_columns)
business_categories['business_id'] = business_categories['business_id'].astype('str')

for i in tqdm(range(business_data.shape[0])):
    temp_cat = business_data.loc[i, 'categories']
    for c in temp_cat:
        business_categories.at[i, c] = 1
    business_categories.at[i, 'business_id'] = business_data.loc[i, 'business_id']

# Deleting business without reviews（55023 -> 55929）
for i in tqdm(range(business_categories.shape[0])):
    if business_categories.loc[i, 'business_id'] not in business_name:
        business_categories.drop(i, inplace=True)
business_categories = business_categories.set_index('business_id')


''' 6. Get categories for user'''
categories_columns = list(categories_set)
categories_columns.sort()
n = len(categories_columns)
user_categories = pd.DataFrame(np.zeros((len(user_name), n + 1)), columns=['user_id'] + categories_columns)
user_categories['user_id'] = user_categories['user_id'].astype('str')
user_categories['user_id'] = user_name
user_categories = user_categories.set_index('user_id')

for i in tqdm(range(review_data.shape[0])):
    business_id, user_id = review_data.loc[i, 'business_id'], review_data.loc[i, 'user_id']
    temp_cat = business_categories.loc[business_id, :]
    user_categories.loc[user_id, :] += temp_cat


''' 7. Normalize user '''
user_categories = (user_categories.T / user_categories.sum(axis=1)).T
user_categories = pd.DataFrame(user_categories, index=user_name, columns=categories_columns)

# Deal with the NaN values in data (because some numbers are divided by 0)
for i in tqdm(range(user_categories.shape[0])):
    if np.isnan(user_categories.iloc[i, 0]):
        user_categories.iloc[i] = [0] * 303


''' 8. Save Data '''
user_categories.to_csv('user_categories.csv')
business_categories.to_csv('business_categories.csv')