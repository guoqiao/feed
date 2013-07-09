# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import task
from . import models as m

@task()
def parse(url):
    try:
        obj = m.Feed.objects.get(url=url)
    except:
        obj = m.Feed(url=url)
    obj.parse()
