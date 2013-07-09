# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from feeds import models as m
from feeds import tasks  as t

class Command(NoArgsCommand):
    help = "parse feeds"

    def handle_noargs(self, **options):
        for feed in m.Feed.objects.all():
            self.stdout.write('parsing %s\n' % feed.title)
            t.parse.delay(feed.url)
