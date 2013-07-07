#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
#from time import mktime
from datetime import datetime
import feedparser as fp
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

def mkdt(struct_time):
    #return datetime.fromtimestamp(mktime(struct_time))
    dt = datetime(*struct_time[:6]) # cool way
    #print 'mkdt:%s-->%s' % (struct_time,dt)
    return dt

class Common(models.Model):
    # info for both feed and item
    title = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    description = models.TextField()
    published = models.DateTimeField(blank=True,null=True)
    born = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-born']

    def __unicode__(self):
        return self.title

class Feed(Common):

    url = models.URLField(unique=True) # rss url
    etag = models.CharField(max_length=50,blank=True) #6c132-941-ad7e3080
    modified = models.DateTimeField(blank=True,null=True)
    parsed = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    tags = TaggableManager(verbose_name='标签',help_text='关键字之间用英文逗号分隔',blank=True)
    users =models.ManyToManyField(User,blank=True)

    class Meta:
        ordering = ['-born']

    def rm_old(self):
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('feed',[self.pk])

    def recent(self):
        return self.item_set.all()[:5]

    def parse(self):
        self.parsed = datetime.now()
        d = fp.parse(self.url,etag=self.etag,modified=self.modified)
        # {'feed': {}, 'bozo': 1, 'bozo_exception': error(10054, ''), 'entries': []}
        if not d:
            print 'parse fail'
            return
        f = d.feed
        if not f:
            if 'bozo' in d:
                print 'bozo:',d.bozo
            if 'status' in d:
                self.status = d.status
                print 'status:',d.status
                self.save()
            print d.debug_message
            return
        if 'etag' in d:
            self.etag = d.etag
        if 'modified_parsed' in d:
            self.modified = mkdt(d.modified_parsed)

        if 'title' in f:
            self.title = f.title
        if 'link' in f:
            self.link = f.link
        if 'description' in f:
            self.description = f.description
        if 'published_parsed' in f:
            self.published = mkdt(f.published_parsed)
        elif d.entries:
            e = d.entries[0] # top one is the most recent one
            if 'published_parsed' in e:
                self.published = mkdt(e.published_parsed)
        if not self.published:
            self.published = datetime.now()
        self.save()
        for e in d.entries:
            if 'link' not in e:
                print 'no link in entry: %s' % e
                continue
            link = e.link
            if Item.objects.filter(link=link).exists():
                print 'link exists: %s' % link
                continue
            item = Item(feed=self,link=link)
            item.title = e.get('title','')
            item.author = e.get('author','')
            item.description = e.get('description','')
            #item.content = e.get('summary_detail','')
            item.make_full_text()
            if 'published_parsed' in e:
                item.published = mkdt(e.published_parsed)
            item.save()

class Item(Common):
    feed = models.ForeignKey(Feed)
    content = models.TextField()
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ['-published','-born']

    @models.permalink
    def get_absolute_url(self):
        return ('item',[self.pk])

    def make_full_text(self):
        url = 'http://ftr.fivefilters.org/makefulltextfeed.php?url=%s' % self.link
        d = fp.parse(url)
        if d.entries:
            e = d.entries[0]
            self.content = e.description
