# -*- coding: UTF-8 -*-
import fabsettings
from fabric.api import *

env.hosts = ['readfree.me']
env.user = fabsettings.USER
env.password = fabsettings.PASSWORD
env.deploy_dir = '/root/readfree'
env.nginx_dir = '/etc/nginx/sites-enabled'

SITE_NAME = 'readfree.me'

import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
        return result

    return timed

def restart():
    with cd(env.nginx_dir):
        run('rm %s' % SITE_NAME)
        run('service nginx reload')
        sudo('supervisorctl restart rf')
        run('ln -s ../sites-available/%s %s' % (SITE_NAME,SITE_NAME))
        run('service nginx reload')
        sudo('supervisorctl restart ce')

def pull():
    with cd(env.deploy_dir):
        run("git pull")
        run('./manage.py collectstatic --noinput')

def pip():
    with cd(env.deploy_dir):
        run("pip install -r requirements/base.txt")
        run("pip install -r requirements/product.txt")

def static():
    with cd(env.deploy_dir):
        run('./manage.py collectstatic --noinput')

def syncdb():
    with cd(env.deploy_dir):
        run('./manage.py syncdb')

def migrate():
    with cd(env.deploy_dir):
        run('./manage.py migrate books')

def up_on():
    with cd(env.nginx_dir):
        run('rm %s' % SITE_NAME)
        run('service nginx reload')

def up_done():
    with cd(env.nginx_dir):
        run('ln -s ../sites-available/%s %s' % (SITE_NAME,SITE_NAME))
        run('service nginx reload')

@timeit
def up():
    with cd(env.deploy_dir):
        run("git pull")
        run('./manage.py syncdb --noinput')
        #run('./manage.py migrate books --noinput')
    restart()
