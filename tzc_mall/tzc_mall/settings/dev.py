"""
Django settings for tzc_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 追加导包路径

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@nie0x^*2e($3f&v+l_h1*u=@hsux9+w*a%1q)6-0fi1qt$l*4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',  # 定时任务
    'users',    # 注册用户app
    'contents',    # 注册首页
    'oauth',    # 注册认证模型
    'areas',    # 注册省份地址
    'goods',    # 注册商品表
    'haystack',    # 全文检索
    'carts',    # 购物车
    'orders',    # 订单
    'payment',    # 支付
    'tzc_admin',    # 后台管理
    'corsheaders',    # 跨域访问
    'rest_framework', # drf
    'rest_framework_jwt', # jwt
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tzc_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # configure Jinja2 templates engine
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # render jinja2 templates environment
            'environment': 'tzc_mall.utils.jinja2_env.jinja2_environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

        },
    },
]

# 指定本项目用户模型类
AUTH_USER_MODEL = 'users.User'

WSGI_APPLICATION = 'tzc_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # database engine
        'HOST': '192.168.137.131',  # database host
        'PORT': 3306,  # port
        'USER': 'tzc',  # username
        'PASSWORD': '123',  # password
        'NAME': 'tzc_mall'  # databasename
    },
    # 'slave': {  # 读（从机）
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': '192.168.137.131',
    #     'PORT': 8306,
    #     'USER': 'root',
    #     'PASSWORD': 'mysql',
    #     'NAME': 'tzc_mall'
    # }
}

# DATABASE_ROUTERS = ['tzc_mall.utils.db_router.MasterSlaveDBRouter']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  #
    'formatters': {  # logger format
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # logger handler
        'console': {  # print
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # output to file
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/tzc_mall.log'),  # the position of logger file
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  #
        'django': {  # define logger that calls django
            'handlers': ['console', 'file'],  # print both console and file
            'propagate': True,  # continue to logger file
            'level': 'INFO',  # print info at least level
        },
    }
}

# django-redis config
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "strict_login": {  # 避免重复登录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.137.131:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# 指定自定义的用户认证后端
AUTHENTICATION_BACKENDS = ['users.utils.CheckAccountModel']

# 跳转login的地址

LOGIN_URL = '/login/'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# oauth中qq的配置信息
QQ_CLIENT_ID = '101518219'  # 随意填写 目前属于开发阶段
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'  # 随意填写 开发阶段
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# configure the static file load path
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'hechaoshuai@yeah.net'  # 授权的邮箱
EMAIL_HOST_PASSWORD = 'OXUSPYKYKGDVCAUA'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = 'tzc_mall<hechaoshuai@yeah.net>'  # 发件人抬头

EMAIL_VERIFY_URL = 'http://127.0.0.1/emails/verification/'

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'tzc_mall.utils.fastdfs.fastdfs_storage.FastDFSStorage'

# 文件路径所在的ip
FDFS_BASE_URL = 'http://192.168.137.131:8888/'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.137.131:9200/',  # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'tzc_mall',  # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

ALIPAY_APPID = '2021000117617112'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'

CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/1 * * * *', 'contents.crons.generate_static_index_html',
     '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
]

CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
'JWT_RESPONSE_PAYLOAD_HANDLER': 'tzc_admin.utils.jwt_response_payload_handler',
}

