import pandas as pd
import numpy as np
from surprise import dump
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def rmse(y_true, y_pred):
    diff = y_true - y_pred
    return 'RMSE', np.sqrt(np.mean(diff ** 2))


def mae(y_true, y_pred):
    return 'MAE', np.mean(np.abs(y_true - y_pred))


def auc(y_true, y_pred):
    y_true = np.where(y_true >= 4, 1, 0)
    y_pred = np.where(y_pred >= 4, 1, 0)
    return 'AUC', roc_auc_score(y_true, y_pred)


def sigma(y_true, y_pred):
    res = np.where(np.abs(y_true - y_pred) <= 1, 1, 0)
    return 'Sigma', np.sum(res) / res.shape[0]


def acc(y_true, y_pred):
    res = np.where(np.abs(y_true - y_pred) == 0, 1, 0)
    return 'ACC', np.sum(res) / res.shape[0]


def predicting(model, test_data, evaluation, round_evaluation):
    test_data = test_data.values
    pred = []
    truth = []
    for row in test_data:
        pred.append(model.predict(row[1], row[0], verbose=False).est)
        truth.append(row[2])
    pred = np.array(pred)
    truth = np.array(truth)

    metrics = []
    for e in evaluation:
        metrics.append(e(truth, pred))
    for e in round_evaluation:
        metrics.append(e(truth, np.round(pred)))
    return pred, truth, metrics


''' 1. Read data'''
data = pd.read_csv('final_matrix.csv')
data = data.drop(columns=['Unnamed: 0'])

business_cat = pd.read_csv('business_categories.csv', index_col=0)
user_cat = pd.read_csv('user_categories.csv', index_col=0)
business_top = pd.read_csv('business_topics.csv', index_col=0)
user_top = pd.read_csv('user_topics.csv', index_col=0)

_, algo = dump.load('model.pickle')

''' 2. Split data for both CF and CB '''
train_data, test_data = train_test_split(data, test_size=0.1, random_state=826)
# print(train_data.shape)
# print(test_data.shape)


''' 3. Test for pure CF'''
y_pred, y_true, metrics = predicting(algo, test_data, [rmse, mae, auc], [acc, sigma])
for name, res in metrics:
    print(name, res)


''' 4. Test for cascade CB + CF '''
top_sim = test_data[['topics_similarity']].values.reshape(-1,)
cat_sim = test_data[['categories_similarity']].values.reshape(-1,)
sim = top_sim + cat_sim
res = y_pred + sim / 4

for metric in [rmse, mae]:
    print(metric(y_true, res))
for metric in [acc, sigma]:
    print(metric(y_true, np.round(res)))
true_label = np.where(y_true >= 4, 1, 0)
res_label = np.where(res > 4, 1, 0)
print(auc(true_label, res_label))