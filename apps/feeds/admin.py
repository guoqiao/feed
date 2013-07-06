#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from . import models as m

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title','description','url','link','published')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('feed','title','description','link','published')

admin.site.register(m.Feed, FeedAdmin)
admin.site.register(m.Item, ItemAdmin)

