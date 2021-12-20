import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def preprocessing_friends(s):
    friends = s.split(sep=', ')
    res = ''
    i = 0
    for f in friends:
        if i == 10:
            break
        res = res + f + ', '
        i += 1
    res = res[:-2]
    return res


''' 1. Read Data '''
csv_path = 'yelp_academic_dataset_user.csv'
data = pd.read_csv(csv_path, low_memory=False)
data = data[['user_id', 'name', 'review_count', 'friends']]
# print(data)


''' 2. Clean Data '''
data['friends'] = data['friends'].apply(preprocessing_friends)


''' 3. Save Data '''
sql_engine = create_engine("mysql+pymysql://root:dbuserdbuser@localhost")
data.to_sql('user', sql_engine, schema='yelp', index=False, if_exists='replace')

data.to_csv('user.csv')