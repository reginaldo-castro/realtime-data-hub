import io
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_data_ingestion_authenticated():
    user = User.objects.create_user(username='teste', password='12345')
    client = APIClient()
    client.force_authenticate(user=user)
    
    fake_file = io.BytesIO(b'Teste,data\n1,2')
    fake_file.name = 'teste.csv'
    
    response = client.post(
        '/api/v1/data/',
        {'file': fake_file},
        format='multipart'
    )

    assert response.status_code == 201
    assert response.data['status'] == 'PENDING'
    
    
@pytest.mark.django_db
def test_data_ingestion_requires_auth():
    client = APIClient()
    
    response = client.post('/api/v1/data/')
    
    assert response.status_code in (401, 403)
    