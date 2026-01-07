import pytest
from data_ingestion.tasks import process_data_job
from data_ingestion.models import DataJob
from django.contrib.auth.models import User
from unittest.mock import AsyncMock


@pytest.mark.django_db
def test_process_data_job(mocker):
    user = User.objects.create_user(username='teste', password='12345')
    job  = DataJob.objects.create(user=user, file='fake.csv')
    
    mock_channel_layer = mocker.Mock()
    mock_channel_layer.group_send = AsyncMock()

    mocker.patch(
        "data_ingestion.tasks.get_channel_layer",
        return_value=mock_channel_layer
    )

    mocker.patch("time.sleep", return_value=None)

    process_data_job(job.id)

    job.refresh_from_db()
    assert job.status == 'DONE'

    assert mock_channel_layer.group_send.called
    

                
            