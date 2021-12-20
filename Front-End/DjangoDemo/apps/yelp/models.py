import json

from django.db import models


# from utils.models import BaseModel
# Create your models here.


class User(models.Model):
    user_id = models.TextField(primary_key=True, verbose_name='user_id', unique=True, db_index=True)
    name = models.TextField(verbose_name='name')
    review_count = models.SmallIntegerField(verbose_name='review_count')
    friends = models.TextField(verbose_name='friends')

    class Meta:
        unique_together = (
            'user_id',
        )
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.user_id + ':' + self.name

    def getJson(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'review_count': self.review_count,
            'friends': self.friends,
        }


def ListBis(listBis):
    res = []
    for i in range(len(listBis)):
        i = json.loads(json.dumps(listBis[i].getJson()))

        print(i)
        print(type(i))
        print(i['business_id'])
        res.append({
            'business_id': i['business_id'],
            'name': i['name'],
            'stars': i['stars'],
            'categories': i['categories'],
        })
    return res


class business(models.Model):
    business_id = models.TextField(primary_key=True, verbose_name='business_id', unique=True, db_index=True)
    name = models.TextField(verbose_name='name')
    city = models.TextField(verbose_name='city')
    address = models.TextField(verbose_name='address')
    stars = models.FloatField(verbose_name='stars')
    review_count = models.SmallIntegerField(verbose_name='review_count')
    is_open = models.SmallIntegerField(verbose_name='is_open')
    categories = models.TextField(verbose_name='categories')
    DogsAllowed = models.SmallIntegerField(verbose_name='DogsAllowed')
    CoatCheck = models.SmallIntegerField(verbose_name='CoatCheck')
    Smoking = models.TextField(verbose_name='Smoking')
    DietaryRestrictions = models.TextField(verbose_name='DietaryRestrictions')
    RestaurantsGoodForGroups = models.SmallIntegerField(verbose_name='RestaurantsGoodForGroups')
    BYOB = models.SmallIntegerField(verbose_name='BYOB')
    Alcohol = models.TextField(verbose_name='Alcohol')
    RestaurantsPriceRange2 = models.FloatField(verbose_name='RestaurantsPriceRange2')

    class Meta:
        unique_together = (
            'business_id',
        )
        db_table = 'business'
        verbose_name = '商业表'
        verbose_name_plural = verbose_name

    def getJson(self):
        return {
            'business_id': self.business_id,
            'name': self.name,
            'stars': self.stars,
            'categories': self.categories,
        }
