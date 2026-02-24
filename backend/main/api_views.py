from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import Resume
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().select_related('owner').prefetch_related(
        'skills', 'education', 'previous_jobs__company', 'ratings'
    )
    serializer_class = ResumeSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'resume_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)  # cache 60 seconds
        return response
