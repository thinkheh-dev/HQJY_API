"""
Django settings for HQJY_API project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%miidy5)f#ku6dq5jt#bq^gj7h@97)y_^+)=*@v1!^+x8n&7ei'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# 替换系统用户模型
AUTH_USER_MODEL = 'users.UserInfo'

# Application definition

INSTALLED_APPS = [
	'xadmin',
	'crispy_forms',
	'reversion',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'DjangoUeditor',
	'service_object.apps.ServiceObjectConfig',
	'enterprise_info.apps.EnterpriseInfoConfig',
	'users.apps.UsersConfig',
	'bg_services.apps.BgServicesConfig',
	'inc_operation.apps.IncOperationConfig',
	'platform_operation.apps.PlatformOperationConfig',
	'user_operation.apps.UserOperationConfig',
	'page_control.apps.PageControlConfig',
	'file_repository.apps.FileRepositoryConfig',
	'django_filters',
	'django_crontab',
	'rest_framework',
	'rest_framework_swagger',
	'corsheaders',
	'rest_framework.authtoken',
	
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

CORS_ORIGIN_ALLOW_ALL = True

CRONJOBS = [

    ('00 00 * * *', "enterprise_info.views.update_stock_status",
     '>> /home/warlock921/MyCode/PycharmProjects/HQJY_API/con_logs/daydata.log'),

]

ROOT_URLCONF = 'HQJY_API.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'HQJY_API.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'hqjy_api_database',
		'USER': 'root',
		'PASSWORD': 'P@ssword',
		'HOST': '192.168.10.205', # 生产数据库
		# 'HOST': 'localhost',  # 测试数据库
		'PORT': '3306',
		# 'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' } ,
	}
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 用户认证配置
AUTHENTICATION_BACKENDS = (
	'users.utils.CustomBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# STATICFILES_DIRS = (
# 	os.path.join(BASE_DIR, "static"),
# )

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	),
	
	# 'DEFAULT_THROTTLE_CLASSES': (
	#     'rest_framework.throttling.AnonRateThrottle',
	#     'rest_framework.throttling.UserRateThrottle'
	# ),
	# 'DEFAULT_THROTTLE_RATES': {
	#     'anon': '2/minute',
	#     'user': '3/minute'
	# }
	
	'DEFAULT_THROTTLE_RATES': {
		'user_change_password_scope': '5/minute',
		'user_realname_auth_scope': '3/day',
		'eps_auth_scope': '3/day',
	},
}

import datetime

JWT_AUTH = {
	'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
	'JWT_AUTH_HEADER_PREFIX': 'JWT',
	'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',  # response中token的payload部分处理函数
}

# 聚合网短信发送API-KEY：
SMS_API_KEY = "95adec9c39fc720b44d7932cdb9a6851"

# 聚合网三网手机实名认证API-KEY：
REAL_API_KEY = "c06b67b14e7fde9dcc99c651d4c024be"

# 聚合网企业工商数据认证API-KEY：
EPS_API_KEY = "0b182de1cea873873ee78233ff64ef52"

# 手机号码正则表达式
REGEX_MOBILE = r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'

# 18位身份证号码正则表达式
REGEX_IDCARD = r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'

'''
参照标准：

《GB_32100-2015_法人和其他组织统一社会信用代码编码规则.》
按照编码规则:
统一代码为18位，统一代码由十八位的数字或大写英文字母（不适用I、O、Z、S、V）组成，由五个部分组成：
第一部分（第1位）为登记管理部门代码，9表示工商部门；(数字或大写英文字母)
第二部分（第2位）为机构类别代码;(数字或大写英文字母)
第三部分（第3-8位）为登记管理机关行政区划码；(数字)
第四部分（第9-17位）为全国组织机构代码；(数字或大写英文字母)
第五部分（第18位）为校验码(数字或大写英文字母)
'''

# 18位企业统一信用代码正则表达式
REGEX_CREDIT = r'^(11|12|13|19|51|52|53|59|91|92|93|Y1)\d{6}\w{9}\w$'

# 支付宝相关配置
# private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
# ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# session 设置
SESSION_COOKIE_AGE = 60 * 30  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

# 添加对svg图片的支持
import mimetypes

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

SWAGGER_SETTINGS = {
	# 基础样式
	'SECURITY_DEFINITIONS': {
		"basic": {
			'type': 'basic'
		}
	},
	# 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
	'LOGIN_URL': 'rest_framework:login',
	'LOGOUT_URL': 'rest_framework:logout',
	# 'DOC_EXPANSION': None,
	'SHOW_REQUEST_HEADERS': True,
	# 'USE_SESSION_AUTH': True,
	'DOC_EXPANSION': 'list',
	# 接口文档中方法列表以首字母升序排列
	'APIS_SORTER': 'alpha',
	# 如果支持json提交, 则接口文档中包含json输入框
	'JSON_EDITOR': True,
	# 方法列表字母排序
	'OPERATIONS_SORTER': 'alpha',
	'VALIDATOR_URL': None,
}
