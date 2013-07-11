#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('feeds.views',
    url(r'^$', 'home', name='home'),
    url(r'^add$', 'add', name='add'),
    url(r'^hot$', 'hot', name='hot'),
    url(r'^mine$', 'mine', name='mine'),
    url(r'^search$', 'search', name='search'),
    url(r'^feed/(?P<pk>\d+)$', 'feed', name='feed'),
    url(r'^feed/(?P<pk>\d+)/delete$', 'feed_delete', name='feed_delete'),
    url(r'^feed/(?P<pk>\d+)/update$', 'feed_update', name='feed_update'),
    url(r'^feed/xfollow$', 'feed_xfollow', name='feed_xfollow'),
    url(r'^item/(?P<pk>\d+)$', 'item', name='item'),
)
