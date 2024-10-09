from celery import shared_task
import time
from .reports import PreferenceListReport
from .models import User

# TODO: Add the result to a separate location, storage, etc
@shared_task
def generate_report_task(user_id):
    user = User.objects.get(pk=user_id)
    print('Start report generation....')
    time.sleep(1)
    pref_report = PreferenceListReport(user)
    print('Finished report generation')
    return {"user_id": user_id, "pdf": pref_report.as_bytes().getvalue()}