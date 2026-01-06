import time
from celery import shared_task
from .models import DataJob

@shared_task
def process_data_job(job_id):
    job = DataJob.objects.get(id=job_id)
    job.status = 'RUNNING'
    job.save()
    
    for i in range(5):
        time.sleep(2)
    
    job.status = 'DONE'
    job.save()