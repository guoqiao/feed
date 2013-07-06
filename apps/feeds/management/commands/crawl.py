# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from time import mktime
import feedparser

from django.core.management.base import NoArgsCommand
from feeds.models import Resource
from feeds.models import Topic

MAX = 10

class Command(NoArgsCommand):
    help = "do crawl"

    def handle_noargs(self, **options):
        for res in Resource.objects.all():
            self.stdout.write('crawling %s\n' % res)
            if res.type != 'rss':
                continue
            res.feed_updated = datetime.now()
            res.save()
            d = feedparser.parse(res.res_url)
            for e in d.entries[:MAX]:
                if Topic.objects.filter(link=e.link):
                    break
                try:
                    seconds = mktime(e.published_parsed)
                    date = datetime.fromtimestamp(seconds)
                except:
                    date = datetime.now()
                t = Topic(
                        res=res,
                        title = e.title,
                        link = e.link,
                        descn = e.description,
                        date = date,
                        )
                t.save()
            # keep 10 only
            topics = res.topic_set.all()
            print topics.count(), MAX
            if topics.count() > MAX:
                date_max = topics[MAX].date
                topics.filter(date__lte=date_max).delete()
                self.stdout.write('delete old done\n')

