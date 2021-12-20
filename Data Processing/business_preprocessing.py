import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def update_enum(s):
    if s is np.nan:
        return s
    elif 'None' in s or 'none' in s:
        return np.nan
    elif s[0] == 'u':
        return s[2:-1]
    elif s[0] == "'":
        return s[1:-1]
    elif s == "u'none'":
        return np.nan


def update_price(s):
    if s is not np.nan and s != 'None':
        return int(s)
    else:
        return np.nan


def dict_clean_bool(s):
    if s is np.nan or s == 'None':
        return np.nan

    global features
    feature_str = ''
    for feature in features:
        if "'" + feature + "': True" in s:
            feature_str = feature_str + feature + ', '
    return feature_str[:-2] if feature_str else np.nan


def dict_categories(s):
    global categories_set
    if s is np.nan or s == 'None' or s == 'none':
        return np.nan
    features = s.split(sep=', ')
    for f in features:
        categories_set.add(f)
    return s


''' 1. Read data'''
csv_path = 'yelp_academic_dataset_business.csv'
data = pd.read_csv(csv_path, low_memory=False)


''' 2. Delete columns related to time'''
for c in data.columns:
    if len(c) > 6 and c[:5] == 'hours':
        print('Delete：', c)
        data.drop(c, axis=1, inplace=True)
for c in ['attributes.Open24Hours', 'hours']
    print('Delete：', c)
    data.drop(c, axis=1, inplace=True)
# print(data.columns)


''' 3. Delete useless columns '''
c_list = ['postal_code', 'state', 'attributes', 'attributes.RestaurantsDelivery', 'attributes.BusinessAcceptsBitcoin',
          'latitude', 'longitude']
for c in c_list:
    data.drop(c, axis=1, inplace=True)
# print(data.columns)


''' 4. Delete the prefix 'attributes.' '''
for c in data.columns:
    if c[:3] == 'att':
        new_c = c[11:]
        data.rename(columns={c: new_c}, inplace=True)
# print(data.columns)


''' 5. Clean the columns with Boolean variable '''
bool_c_list = ['DogsAllowed', 'CoatCheck', 'RestaurantsGoodForGroups', 'BYOB', 'RestaurantsTableService',
               'RestaurantsCounterService',
               'Corkage', 'GoodForKids', 'HappyHour', 'WheelchairAccessible', 'BusinessAcceptsCreditCards',
               'ByAppointmentOnly', 'DriveThru',
               'GoodForDancing', 'Caters', 'AcceptsInsurance', 'RestaurantsReservations', 'RestaurantsTakeOut',
               'BikeParking',
               'OutdoorSeating', 'HasTV']
for c in bool_c_list:
    data[c].replace('False', False, inplace=True)
    data[c].replace('True', True, inplace=True)
    data[c].replace('None', np.nan, inplace=True)

data['is_open'].replace(0, False, inplace=True)
data['is_open'].replace(1, True, inplace=True)


''' 6. Clean the columns with Enum variable '''
enum_c_list = ['Smoking', 'AgesAllowed', 'Alcohol', 'BYOBCorkage', 'NoiseLevel', 'WiFi', 'RestaurantsAttire']
for c in enum_c_list:
    data[c] = data[c].apply(update_enum)
data['RestaurantsPriceRange2'] = data['RestaurantsPriceRange2'].apply(update_price)


''' 7. Clean the columns with Dictionary variable '''
dict_c_list = ['DietaryRestrictions', 'HairSpecializesIn', 'Ambience', 'BestNights', 'Music', 'BusinessParking',
               'GoodForMeal']
feature_ls = [['dairy-free', 'gluten-free', 'vegan', 'kosher', 'halal', 'soy-free', 'vegetarian'],
              ['straightperms', 'coloring', 'extensions', 'africanamerican', 'curly', 'kids', 'perms', 'asian'],
              ['touristy', 'hipster', 'romantic', 'divey', 'intimate', 'trendy', 'upscale', 'classy', 'casual'],
              ['monday', 'tuesday', 'friday', 'wednesday', 'thursday', 'sunday', 'saturday'],
              ['dj', 'background_music', 'no_music', 'jukebox', 'live', 'video', 'karaoke'],
              ['garage', 'street', 'validated', 'lot', 'valet'],
              ['dessert', 'latenight', 'lunch', 'dinner', 'brunch', 'breakfast']
              ]

for i, c in enumerate(dict_c_list):
    features = feature_ls[i]
    data[c] = data[c].apply(dict_clean_bool)

categories_set = set()
data['categories'] = data['categories'].apply(dict_categories)
# print(categories_set)


''' 8. Delete useless columns '''
c_list = ['AgesAllowed', 'HairSpecializesIn', 'RestaurantsCounterService', 'GoodForDancing', 'AcceptsInsurance', 'RestaurantsTakeOut']
for c in c_list:
    data.drop(c,axis=1, inplace=True)
# print(data.columns)


''' 9. Delete businesses which are not restaurants '''
data = data[data['categories'].str.contains('Restaurants|Bar', case=False, na=False)]
print('The number of restaurant：', data.shape[0])


''' 10. Save data '''
data = data[
    ['business_id', 'name', 'city', 'address', 'stars', 'review_count', 'is_open', 'categories',
     'DogsAllowed', 'CoatCheck', 'Smoking',
     'DietaryRestrictions', 'RestaurantsGoodForGroups', 'BYOB', 'Alcohol',
     'RestaurantsPriceRange2', 'RestaurantsTableService',
     'Corkage', 'GoodForKids', 'HappyHour',
     'WheelchairAccessible', 'BusinessAcceptsCreditCards', 'BYOBCorkage',
     'Ambience', 'BestNights',
     'ByAppointmentOnly', 'NoiseLevel', 'DriveThru', 'HasTV', 'WiFi',
     'Music', 'BusinessParking', 'RestaurantsAttire',
     'GoodForMeal', 'Caters',
     'RestaurantsReservations', 'BikeParking',
     'OutdoorSeating']]

sql_engine = create_engine("mysql+pymysql://root:dbuserdbuser@localhost")
data.to_sql('business', sql_engine, schema='yelp', index=False, if_exists='replace')

data.to_csv('business.csv')

categories_np = np.array(list(categories_set))
np.save('categories.npy', categories_np)