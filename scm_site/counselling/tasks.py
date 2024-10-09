from celery import shared_task
import time
import base64
from .reports import PreferenceListReport
from .models import User

@shared_task
def generate_report_task(user_id):
    user = User.objects.get(pk=user_id)
    print('Start report generation....')
    time.sleep(10)
    pref_report = PreferenceListReport(user)
    print('Finished report generation')
    return {"user_id": user_id, "pdf": base64.b64encode(pref_report.as_bytes().getvalue()).decode('utf-8')}