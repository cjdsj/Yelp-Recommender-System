# Yelp-Recommender-System
Yelp Recommender System - Your Best Restaurant Finder
____________________________________________________________________________________
## Dependencies
Requires following packages for json_to_csv_converter.py (using python2):  
* csv
* simplejson

Requires following packages for other data processing codes:  
* numpy
* pandas
* surprise
* sklearn
* tqdm
* sqlalchemy

## Introduction
Due to the increasing number of users and the rapid expansion of information, the problem of sparsity of data matrix in traditional collaborative filtering (CF) 
becomes more and more prominent. Also, the traditional contentbased filtering (CB) has the problem of lacking novelty in recommendation results. 
Therefore, we propose a new hybrid recommendation method with the combination collaborative filtering and content-based filtering. We use CF to
get rough recommendations, then use CB to get more accurate recommendation based on that. We implement our hybrid recommendation system on yelp restaurants recommendation
task.

## Dataset
We use public Yelp dataset (https://www.yelp.com/dataset). The Yelp dataset is a subset of our businesses, reviews, and user data for use in personal, educational, and academic purposes. We choose Reviews.csv, Business.csv, and Users.csv which are 8.7 GB in total. After preprocessing and only focus on restaurants, we still remain 3,800,000+ reviews, 55,000+ restaurants, 290,000+ users

## Usage
### 1. json_to_csv_converter.py
Provided by Yelp, it is used for converting .json files to .csv files for subsequent processing. There was a little bug in it so I submit a correct version. 
Please note that this code should be runned in Python2.

### 2. business_preprocessing.py
Implement data clean on 'yelp_academic_dataset_business.csv'. It save the preprocessed data as 'business.csv'.

### 3. user_preprocessing.py
Implement data clean on 'yelp_academic_dataset_user.csv'. It save the preprocessed data as 'user.csv'.

### 4. review_preprocessing.py
Implement data clean on 'yelp_academic_dataset_review.csv'. It save the preprocessed data as 'review.csv'.

### 5. LDA.py
Conduncted LDA by PySpark, save the topics for each review as npy file.

### 6. topics.py
Use topics given by LDA algorithm for each topic, we can get topics for every users and business. The data will be stored as 
'user_topics.csv' and 'business_topics.csv'.

### 7. categories.py
We can get categories for each business in 'business.csv', then we can aggregate them to get categories for users. The data will be stored as 
'user_topics.csv' and 'business_topics.csv'.

### 8. sentiment.py
Use Vadar to get the sentiment of each review and save as 'sentiment.csv'.

### 9. final_preprocessing.py
Compute category similarity and topic similarity between all users and businesses using cosine similarity. The data will be stored as 
'final_matrix.csv'.

### 10. train.py
Train the CF model and save it.

### 11. test.py
Test the pure CF method and our hybrid method, show metrics for both methods.

## Website
### 1. Frontend
We built Frontend by Vue.
### 2. Backend
We used Django to build backend. You should put business_categories.csv, business_topics.csv, user_categories.csv, user_topics.csv, 
and model.pickle in this folder to run the backend. All these files can be got from the codes we provided.
### 3. Demo
We desgined four pages in total.\
The first page is the main page, users can type their user id in the input box.\
\
![image](Demo%20img/main_page.png)\
\
We store business and user data as tables in database, and we use MySQL to visit them. If the user has signed up for yelp, 
which means we can find his/her information in databse, we can show his/her user ID and username on the top left corner.
Then, our hybrid algorithm can find ten restaurants as recommendations based user's history records.\
\
![image](Demo%20img/recommendations_known.png)\
\
If the user is a new user for Yelp, we built a page for him/her to choose some categories that the user is interested in.\
\
![image](Demo%20img/select_categories.png)\
\
And we implemented pure content-based filtering algorithm to do recommendations. That's how we use CB to deal with the problem of cold-start.\
\
![image](Demo%20img/recommendations_unknown.png)
