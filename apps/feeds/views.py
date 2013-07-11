#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string as r2s
from annoying.functions import get_object_or_None
from annoying.decorators import ajax_request
from . import models as m
from . import forms  as f
from . import tasks  as t

def home(request):
    objs = m.Feed.objects.all()
    ctx = {'objs': objs}
    ctx['css_home'] = 'active'
    return render(request, 'feeds/home.html', ctx)

def search(request):
    objs = m.Feed.objects.all()
    q = request.GET.get('q','')
    if q:
        q0 = Q(title__icontains=q)
        q1 = Q(description__icontains=q)
        objs = objs.filter(q0|q1).distinct()
    ctx = {'objs': objs}
    ctx['css_search'] = 'active'
    ctx['q'] = q
    return render(request, 'feeds/home.html', ctx)

@login_required
def hot(request):
    objs = m.Feed.objects.all().annotate(count=Count('users')).filter(count__gt=0).order_by('-count','-born')
    ctx = {'objs': objs}
    ctx['css_hot'] = 'active'
    return render(request, 'feeds/home.html', ctx)

@login_required
def mine(request):
    objs = request.user.feed_set.all()
    ctx = {'objs': objs}
    ctx['css_mine'] = 'active'
    return render(request, 'feeds/home.html', ctx)

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
    ctx['css_add'] = 'active'
    return render(request, 'feeds/add.html', ctx)
