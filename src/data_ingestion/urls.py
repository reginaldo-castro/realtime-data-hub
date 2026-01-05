from django.urls import path
from .views import DataingestionView

urlpatterns = [
    path('data/', DataingestionView.as_view(), name='data-ingestion'),
]
    