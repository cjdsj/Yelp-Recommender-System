from django.template.context_processors import request
from django.urls import path
from . import views

app_name = 'yelp'

urlpatterns = [

    path('FindUid', views.FindUid),
    path('apiFindUid', views.apiFindUid),
    path('apiBusiness', views.apiFindBusiness)
]