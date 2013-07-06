#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import os, sys
from path import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

HOME = path('~').expanduser()

FILE = path(os.path.abspath(__file__))
HERE = FILE.parent
PROJ_ROOT = HERE.parent
PROJ_NAME = PROJ_ROOT.name
APPS_ROOT = PROJ_ROOT/'apps'

sys.path.insert(0, PROJ_ROOT)
sys.path.insert(0, APPS_ROOT)

ADMINS = (
    ('Guo Qiao', 'guoqiao@gmail.com'),
)

MANAGERS = (
    ('Guo Qiao', 'guoqiao@gmail.com'),
    #('Phoebe', 'phoebe.exe@gmail.com'),
)

#INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJ_ROOT/'sqlite.db',   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJ_ROOT/'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJ_ROOT/'static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # PROJ_ROOT/'static', # static dir use for collect
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'aih(b6j-7x^$4l8b$su7z%m+f158@9pke($k!sj!u3@0cwe-nb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJ_ROOT/'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.webdesign',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',

    'djcelery',
    'kombu.transport.django',
    #'south',
    #'mailer',
    'taggit',
    #'json_field',
    #'django_extensions',

    'statics',
    #'accounts',
    'feeds',
)

import djcelery
djcelery.setup_loader()
BROKER_URL = 'django://'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

FIXTURE_DIRS = (
    PROJ_ROOT/'fixtures',
)

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request", # for request.path in next
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

# == EMAIL ==
EMAIL_HOST='smtp.exmail.qq.com'
EMAIL_USE_TLS=False
EMAIL_PORT=25 # 465 for tls
EMAIL_HOST_USER= 'noreply@guoqiao.me'
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
SERVER_EMAIL=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD='123456' # fill this in local.py
EMAIL_SUBJECT_PREFIX='[readfree.me]'

# == EMIAL for Kindle only
#K_EMAIL_HOST='smtp.readfree.me'
K_EMAIL_HOST='smtp.exmail.qq.com'
K_EMAIL_USE_TLS=False
K_EMAIL_PORT=25
K_EMAIL_HOST_USER='noreply@readfree.me'
K_EMAIL_HOST_PASSWORD='123456' # fill this in local.py

# ==alipay==

ALIPAY_INPUT_CHARSET = 'utf-8'

# 安全检验码，以数字和字母组成的32位字符
ALIPAY_SIGN_TYPE = 'MD5'
ALIPAY_KEY = '' # in local.py

# 合作身份者ID，以2088开头的16位纯数字
ALIPAY_PARTNER = '' # in local.py

# 签约支付宝账号或卖家支付宝帐户
ALIPAY_SELLER_EMAIL = 'guoqiao@gmail.com'

# 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
ALIPAY_RETURN_URL = 'payment_return_url'

# 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
ALIPAY_NOTIFY_URL = 'payment_notify_url'

ALIPAY_SHOW_URL = 'accounts:pro'

# 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
ALIPAY_TRANSPORT = 'https'

LOGGING_PAYMENT = PROJ_ROOT/'payment.log'

# == readfree ==
CONTENT_EXTS = ('mobi','pdf','epub','txt','azw','azw3')
CONTENT_TYPES = (
    'pdf','x-mobipocket-ebook','epub+zip','plain','octet-stream',
)

MAX_UPLOAD_SIZE_M = 30
MAX_UPLOAD_SIZE_B = MAX_UPLOAD_SIZE_M * 1024 * 1024
DAILY_LIMIT = 6

DIY_PREFIX = 'DIY'
