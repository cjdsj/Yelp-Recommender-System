首相修改数据库配置

在setting.py目录下面

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yelp',     # 数据库名称
        'USER': 'root',     # 数据库用户名
        'PASSWORD': 'root',     # 数据库密码
        'HOST': '127.0.0.1',  # 主机地址
        'PORT': 3306                # 端口号
    }
}



运行Django项目

 python manage.py runserver  0.0.0.0:8000



