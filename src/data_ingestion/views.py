from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import DataJob
from .serializers import DataJobSerializer
from .tasks import process_data_job

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
        
 
