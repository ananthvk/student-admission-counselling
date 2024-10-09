from celery import shared_task
import time

@shared_task
def generate_report_task():
    print('Start report generation....')
    time.sleep(10)
    print('Finished report generation')
    