import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


from apps.Result import Result
from apps.yelp.IntelligentSearch import Search, push
from apps.yelp.models import User, business, ListBis


def apiFindUid(request):
    request.encoding = 'utf-8'
    # try:
    # print(request.body)  # b"{username:admin}"
    # print(json.loads(request.body))  # admin
    # print(json.loads(request.body).get('uid'))
    if 'uid' in json.loads(request.body) and json.loads(request.body).get('uid'):
        uid = json.loads(request.body).get('uid')
        # message = '你搜索的内容为: ' + request.GET['uid']
        for i in User.objects.filter(user_id=uid):
            return JsonResponse(Result().renderSuccess(i.getJson()))
    return JsonResponse(Result().renderError("数据输入有误"))
    # except IOError:
    #     return JsonResponse(Result().renderError("数据输入有误"))
    return JsonResponse(Result().renderError())


def FindUid(request):
    return render(request, 'index.html')


def apiFindBusiness(request):
    request.encoding = 'utf-8'
    uid = None
    listB = []
    if 'user_id' in json.loads(request.body) and json.loads(request.body).get('user_id'):
        uid = json.loads(request.body).get('user_id')
        print(uid)  # 这是获取的uid
        """
        填写智能获取的算法 假设算法获取的是s
        """
        listB = Search(uid)

    if 'region' in json.loads(request.body) and json.loads(request.body).get('region'):
        region = json.loads(request.body).get('region')
        print(region)

        print(type(region))
        listB = push(region)
    print(listB)
    # s = ['jFYIsSb7r1QeESVUnXPHBw', 'Of6xu3pY3eHe2yhiyz2dvg', 'z-0oY7VxQMQw3JHvdPejrA', 'EGZ0fhB9k0ZlI5sHda4vFw',
    #      'ZA3u0Nu5V6TqkcYh8U0zdg', 'XDv29FffNd2dWnDOtZP-wg', 'OfA_4cHgvlknHMcn0qNs2w', 'diB_y_0tPzz-OAe5xgFXtw',
    #      'm_a0-8_wR1ypvZzDGeSIgA', 'bBNCUzEJZn8ASQ5LNWOHEg']  # 计算要获取的s
    r = BusinessList(listB)
    if len(r) > 0:
        return JsonResponse(Result().renderSuccess(r))  # 返回计算出来的数据

    return JsonResponse(Result().renderError())


def BusinessList(l):
    q = None
    n = 0
    while True:
        if n == 0:
            q = Q(business_id=l[n])
        elif n == len(l):
            listBu = ListBis(business.objects.filter(q).all())
            return listBu
        else:
            q = q | Q(business_id=l[n])
        n += 1
