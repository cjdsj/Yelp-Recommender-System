import os
import numpy as np
import pandas as pd
from tqdm import tqdm


''' 1. Read reviews data (with sentiment and without text) and LDA data'''
review_data = pd.read_csv('sentiment.csv')
review_data = review_data.drop(columns=['Unnamed: 0'])

lda_file_ls = [int(file_name[:-4]) for file_name in os.listdir(os.getcwd())]
lda_file_ls.sort()


''' 2. Generate topics matrices for user and business '''
business_name = review_data.loc[:, 'business_id'].unique()
business_name = business_name.tolist()
business = pd.DataFrame(np.zeros((len(business_name), 10)), index=business_name)

user_name = review_data.loc[:, 'user_id'].unique()
user_name = user_name.tolist()
user = pd.DataFrame(np.zeros((len(user_name), 10)), index=user_name)


''' 3. Fill topics matrices '''
LDA_THRESHOLD = 0.3
root_path = 'E:/AAA学习/Columbia University/2021 Fall/Big Data Analytics/Homework/Project/Dataset/LDA'
idx = 0

for lda_file_name in tqdm(lda_file_ls):
    lda_file_name = root_path + '/' + str(lda_file_name) + '.npy'
    lda = np.load(lda_file_name)
    for row in lda:
        row = np.where(row>LDA_THRESHOLD, 1, 0)
        user_id, business_id = review_data.loc[idx, 'user_id'], review_data.loc[idx, 'business_id']
        compound = review_data.loc[idx, 'compound']
        user.loc[user_id, :] += row
        business.loc[business_id, :] += row * compound
        idx += 1


''' 4. Normalize topic matrices'''
# user
USER_THRESHOLD = 0.2
user = (user.T / user.sum(axis=1)).T
user = np.where(user >= USER_THRESHOLD, 1, 0)
user = pd.DataFrame(user, index=user_name)

# business
business_count = pd.Series(np.zeros(len(business_name)), index=business_name)
for i in tqdm(range(review_data.shape[0])):
    business_id = review_data.loc[i, 'business_id']
    business_count[business_id] += 1

business = (business.T / business_count).T


''' 5. Save data '''
user.to_csv('user_topics.csv')
business.to_csv('business_topics.csv')