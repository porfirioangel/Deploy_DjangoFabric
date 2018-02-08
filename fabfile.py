from fabric.context_managers import settings, cd, prefix
from fabric.contrib import files
from fabric.api import env, run
from contextlib import contextmanager as _contextmanager

env.directory = '~/TallerDjangoREST'
env.password = 'vagrant'
env.git_user = 'user'
env.git_pass = 'pass'
env.git_repo = 'https://gitlab.com/porfirioads/TallerDjangoREST.git'
env.git_prompt = {
    "Username for 'https://gitlab.com': ": env.git_user,
    "Password for 'https://%s@gitlab.com': " % (env.git_user): env.git_pass
}


def deploy():
    get_source_code()
    get_python_dependencies()
    run_project()


def get_source_code():
    with settings(prompts=env.git_prompt):
        if files.exists(env.directory):
            with cd(env.directory):
                run('git pull origin master')
        else:
            run('git clone %s' % (env.git_repo))


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix('source venv/bin/activate'):
            yield


def get_python_dependencies():
    with virtualenv():
        run('pip install -r requirements.txt')


def run_project():
    with virtualenv():
        run('python manage.py runserver 0.0.0.0:8000 &')
