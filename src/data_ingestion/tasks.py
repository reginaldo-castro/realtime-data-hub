import time
from celery import shared_task
from .models import DataJob
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@shared_task
def process_data_job(job_id):
    channel_layer = get_channel_layer()
    group_name = f'job_{job_id}'
    
    job = DataJob.objects.get(id=job_id)
    job.status = 'PROCESSING'
    job.save()
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'job_update',
            'data':{'status': 'PROCESSING'}
        }
    )
    
    for progresso in range(0, 101, 20):
        time.sleep(1)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'job_update',
                'data': {'progress': progresso}
            }
        )
    
    job.status = 'DONE'
    job.save()
    
    async_to_sync(channel_layer.group_send)(
        group_name,{
            'type': 'job_update',
            'data': {'status': 'DONE'}
        }
    )
