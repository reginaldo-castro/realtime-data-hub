from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from .models import DataJob
from .serializers import DataJobSerializer
from .tasks import process_data_job
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary='Ingestão de dados',
    description = 'Endpoint para upload de arquivos e criação de jobs de processamento.'
)
class DataingestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        
        if not file:
            return Response(
                {"error": "File is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        job = DataJob.objects.create(
                user=request.user, 
                file=file
            )
        
        process_data_job.delay(str(job.id))
                
        serializer = DataJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DataJobPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'


@method_decorator(cache_page(60 * 2), name='dispatch')
class DataJobListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataJobSerializer
    pagination_class = DataJobPagination
    
    def get_queryset(self):
        return DataJob.objects.filter(user=self.request.user).order_by('-created_at')
    

class DataJobDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataJobSerializer
    
    def get_queryset(self):
        return DataJob.objects.filter(user=self.request.user)