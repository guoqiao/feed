#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models as m
from . import forms  as f
from . import tasks  as t

def home(request):
    objs = m.Feed.objects.all()
    return render(request, 'home.html', {'objs': objs})

def feed(request,pk):
    obj = m.Feed.objects.get(pk=pk)
    return render(request, 'feed.html', {'obj': obj})

@login_required
def feed_delete(request,pk):
    obj = m.Feed.objects.get(pk=pk)
    obj.delete()
    messages.success(request,'删除成功')
    return redirect('home')

def item(request,pk):
    obj = m.Item.objects.get(pk=pk)
    return render(request, 'item.html', {'obj': obj})

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
    return render(request, 'add.html', ctx)
