import os
import pandas as pd
import numpy as np
from surprise import dump
from sklearn.metrics.pairwise import cosine_similarity

Path = os.path.dirname(os.path.realpath(__file__))


def Search(input_user_id):
    ''' 1. Read Data '''
    # input_user_id = '0kA0PAJ8QFMeveQWHFqz2A'  # Get from the input of website
    print(Path)
    business_cat = pd.read_csv(Path + '\\data\\business_categories.csv', index_col=0)
    user_cat = pd.read_csv(Path + '\\data\\user_categories.csv', index_col=0)
    business_top = pd.read_csv(Path + '\\data\\business_topics.csv', index_col=0)
    user_top = pd.read_csv(Path + '\\data\\user_topics.csv', index_col=0)
    business_set = business_top.index.values

    ''' 2. CF '''
    model_filename = Path + '\\data\\model.pickle'
    _, cf_algo = dump.load(model_filename)

    result = []
    for business_id in business_set:
        result.append(cf_algo.predict(input_user_id, business_id, verbose=False).est)
    result = pd.Series(result, business_set)
    result = result.sort_values(ascending=False)
    result = pd.DataFrame(result[:50], columns=['CF'])

    ''' 3. Get topics and categories of users and business, weight them '''
    user_topics = user_top.loc[input_user_id, :].values.reshape(1, -1)
    user_categories = user_cat.loc[input_user_id, :].values.reshape(1, -1)

    for business_id in result.index:
        business_topics = business_top.loc[business_id, :].values.reshape(1, -1)
        business_categories = business_cat.loc[business_id, :].values.reshape(1, -1)
        top_sim = cosine_similarity(user_topics, business_topics)[0][0]
        cat_sim = cosine_similarity(user_categories, business_categories)[0][0]
        result.at[business_id, 'top_sim'] = top_sim
        result.at[business_id, 'cat_sim'] = cat_sim
        result.at[business_id, 'final_result'] = result.at[business_id, 'CF'] + 2.5 * (top_sim + cat_sim)

    ''' 4. Find the top 10 restaurants '''
    result = result.sort_values(by='final_result', ascending=False).iloc[:10].index.tolist()
    return result  # List of business_id


def push(categories):
    ''' 1. Read Data '''
    # categories = ['Pizza', 'Seafood', 'Chinese', 'Vegetarian']  # Get from the input of website
    business_cat = pd.read_csv(Path + '\\data\\business_categories.csv', index_col=0)

    ''' 2. Generate user's categories '''
    user_cat = pd.Series([0] * business_cat.shape[1], business_cat.columns)
    for c in categories:
        user_cat[c] = 1

    ''' 3. Compute similarity '''
    res = np.array([])
    u = user_cat.values.reshape(1, -1)
    for business_id in business_cat.index:
        b = business_cat.loc[business_id, :].values.reshape(1, -1)
        temp_res = cosine_similarity(u, b)[0][0]
        res = np.append(res, temp_res)
    res = pd.Series(res, business_cat.index)

    ''' 4. Find the top 10 restaurants '''
    res = res.sort_values(ascending=False)[:10].index.tolist()
    return res  # List of business_id
