#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from base import *
DEBUG = False
SITE_ID = 2
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS += (
    'gunicorn',
)
