from os import symlink
from os.path import join
from os.path import abspath

from contextlib import contextmanager

from fabric.api import env
from fabric.api import lcd
from fabric.api import local
from fabric.api import prefix

env.proj_dir = 'ytlist/'
env.venv_dir = 'venv/'
env.venv_path = abspath(join(env.venv_dir, 'bin/activate/'))

env.bower = 'node_modules/bower/bin/bower --config.interactive=false'

env.bower_dir = 'bower_components/'
env.assets_dir = join(env.proj_dir, 'ytlist/assets/')
env.symlinks = [{'src': join(env.bower_dir, 'bootstrap/less/'),
                 'dst': join(env.assets_dir, 'css/bootstrap')},
                {'src': join(env.bower_dir, 'jquery/dist/jquery.js'),
                 'dst': join(env.assets_dir, 'js/jquery.js')},
                {'src': join(env.bower_dir, 'jquery-cookie/jquery.cookie.js'),
                 'dst': join(env.assets_dir, 'js/jquery.cookie.js')},
                {'src': join(env.bower_dir, 'handlebars/handlebars.js'),
                 'dst': join(env.assets_dir, 'js/handlebars.js')}]

@contextmanager
def virtualenv():
    with prefix('source {}'.format(env.venv_path)):
        yield

def install():
    print('Checking if virutalenv is present...')
    local('virtualenv --version')
    print('Checking if npm is present...')
    local('npm --version')
    print('Environment appears okay, installing.')
    local('virtualenv {}'.format(env.venv_dir))
    with virtualenv():
        local('pip install requests==2.3.0')
        local('pip install django==1.6.2')
        local('pip install django_gears==0.7')
        local('pip install gears-less==0.3.3')
        local('npm install bower')
        local('{} install bootstrap#3.1.1'.format(env.bower))
        local('{} install jquery-cookie#1.4.1'.format(env.bower))
        local('{} install handlebars#1.3.0'.format(env.bower))
        for pair in env.symlinks:
            try:
                symlink(abspath(pair['src']), abspath(pair['dst']))
            except OSError:
                print("Failed linking {} to {}, check if the destintation "
                      "aready exists, and whether you have the correct "
                      "privileges.".format(pair['src'], pair['dst']))
        with lcd(env.proj_dir):
            local('python manage.py syncdb')

def run():
    with virtualenv():
        with lcd(env.proj_dir):
            local('python manage.py runserver')

