from django.urls import path
from .views import DataingestionView, DataJobListView, DataJobDetailView

urlpatterns = [
    path('data/', DataingestionView.as_view(), name='data-ingestion'),
    path('data/jobs/', DataJobListView.as_view(), name='data-job-list'),
    path('data/jobs/<int:pk>/', DataJobDetailView.as_view(), name='data-job-detail'),
]
    