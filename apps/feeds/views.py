#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string as r2s
from annoying.functions import get_object_or_None
from annoying.decorators import ajax_request
from . import models as m
from . import forms  as f
from . import tasks  as t

def home(request):
    objs = m.Feed.objects.all()
    return render(request, 'feeds/home.html', {'objs': objs})

def feed(request,pk):
    obj = m.Feed.objects.get(pk=pk)
    return render(request, 'feeds/feed.html', {'obj': obj})

@login_required
def feed_update(request,pk):
    obj = m.Feed.objects.get(pk=pk)
    obj.item_set.all().delete()
    obj.etag = ""
    obj.modified = None
    obj.save()
    t.parse.delay(obj.url)
    messages.success(request,'正在更新')
    url = request.GET.get('next','home')
    return redirect(url)

@ajax_request
@login_required
def feed_xfollow(request):
    pk = request.GET.get('pk','')
    obj = m.Feed.objects.get(pk=pk)
    user = request.user
    if user in obj.users.all():
        obj.users.remove(user)
        x = ''
    else:
        obj.users.add(request.user)
        x = 'un'
    template = 'feeds/feed_btn_%sfollow.html' % x
    html = r2s(template,{})
    return {'ret':'ok','html':html}

@login_required
def feed_delete(request,pk):
    obj = m.Feed.objects.get(pk=pk)
    obj.delete()
    messages.success(request,'删除成功')
    return redirect('home')

def item(request,pk):
    obj = m.Item.objects.get(pk=pk)
    return render(request, 'feeds/item.html', {'item': obj})

def add(request):
    F = f.FeedForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            t.parse.delay(feed.url)
            messages.info(request,'正在解析,稍等片刻:)')
            return redirect('home')
    ctx = {'form':form}
    return render(request, 'feeds/add.html', ctx)
