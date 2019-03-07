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
	'django_filters',
	'rest_framework',
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
		#'HOST': 'localhost',
		'HOST': '192.168.10.205',
		'PORT': '3306',
		#'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' } ,
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

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static"),
)

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
	},
	
}

import datetime

JWT_AUTH = {
	'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
	'JWT_AUTH_HEADER_PREFIX': 'JWT',
	'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',  # response中token的payload部分处理函数
}

# 云片网短信发送API-KEY：
#API_KEY = "ff2cf8283b3eb184e767c7c21dd5c165"
API_KEY = "04049cb7d221836ae7eb5eb5150f3417"


# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

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

#添加对svg图片的支持
import mimetypes
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)
