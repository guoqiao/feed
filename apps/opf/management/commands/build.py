# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import subprocess
from shutil import copyfile
from path import path
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
#from feeds import models as m
from django.conf import settings
from django.template.loader import render_to_string as r2s

HERE = path(os.path.abspath(__file__)).parent
OPF = HERE.parent.parent/'templates'/'opf'
OUT = settings.PROJ_ROOT/'out'

def build_for_user(user):
    print 'building for user:%s' % user
    out = OUT # TODO
    for doc in OPF.walkfiles():
        rp = OPF.relpathto(doc)
        r = out/rp
        r.parent.makedirs_p()
        if doc.ext in ['.html','.opf','.ncx']:
            print 'rendering',rp
            s = r2s(doc,{'user':user})
            r.write_text(s,encoding='utf-8')
        else:
            print 'copying',rp
            copyfile(doc,r)
    cmd = 'kindlegen %s' % (OUT/'content.opf',)
    subprocess.call(cmd.split())


class Command(NoArgsCommand):
    help = "parse feeds"

    def handle_noargs(self, **options):
        for user in User.objects.all():
            if user.feed_set.count < 1:
                continue
            build_for_user(user)
