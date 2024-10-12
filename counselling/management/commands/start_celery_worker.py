import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload

def restart_celery():
    cmd = 'pkill -f "celery worker"'
    subprocess.call(shlex.split(cmd))
    cmd = 'watchmedo auto-restart --directory=./ --pattern=*.py --ignore-pattern=**/test/** --recursive -- celery -A scm_site worker --loglevel=INFO'
    #cmd = 'python -m celery -A scm_site worker -l info'
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker....')
        # autoreload.run_with_reloader(restart_celery)
        restart_celery()