import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from surprise import Reader
from surprise import Dataset
from surprise import SVD
from surprise import dump
from surprise.model_selection import GridSearchCV


def grid_search_para(train_data):
    print("> Creating trainset...")
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(train_data[['user_id', 'business_id', 'stars']], reader)
    print("> Training trainset...")
    param_grid = {
        "n_factors": [80, 100, 120],
        "n_epochs": [20, 40],
        "lr_all": [0.005, 0.05, 0.5],
        "reg_all": [0.02, 0.08, 0.1]
    }
    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], refit=True, cv=5, joblib_verbose=2)
    gs.fit(data)

    print("BEST RMSE: \t", gs.best_score["rmse"])
    print("BEST MAE: \t", gs.best_score["mae"])
    print("BEST params: \t", gs.best_params["rmse"])


''' 1. Read data'''
data = pd.read_csv('final_matrix.csv')
data = data.drop(columns=['Unnamed: 0'])

business_cat = pd.read_csv('business_categories.csv', index_col=0)
user_cat = pd.read_csv('user_categories.csv', index_col=0)
business_top = pd.read_csv('business_topics.csv', index_col=0)
user_top = pd.read_csv('user_topics.csv', index_col=0)


''' 2. Split data for both CF and CB '''
train_data, test_data = train_test_split(data, test_size=0.1, random_state=826)
# print(train_data.shape)
# print(test_data.shape)


''' 3. Grid search for best hyper parameters for CF '''
grid_search_para(train_data)


''' 4. Train the CF model using the best hyper parameters '''
print("> Creating trainset...")
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(train_data[['user_id', 'business_id', 'stars']], reader)
trainset = data.build_full_trainset()

print("> Training trainset...")
algo = SVD(n_factors=80, n_epochs=40, lr_all=0.005, reg_all=0.1)
algo.fit(trainset)


''' 5. Save CF model '''
model_filename = "model.pickle"
print(">> Starting dump")
dump.dump(model_filename, algo=algo)
print(">> Dump done")