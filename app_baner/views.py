from rest_framework import generics, permissions, response, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from.models import Baner
from .serializers import BanerSerializer

from rest_framework import status
from django.core.cache import cache



CACHE_KEY = 'baner_list'
CACHE_TIMEOUT = 60 * 15


class BanerListView(APIView):
    def get(self, request):
        data = cache.get(CACHE_KEY)
        
        if not data:
            queryset = Baner.objects.all()
            serializer = BanerSerializer(queryset, many=True)
            data = serializer.data
            cache.set(CACHE_KEY, data, timeout=CACHE_TIMEOUT)
        
        return response.Response(data)



class BanerCreateView(APIView):
    def post(self, request):
        serializer = BanerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            queryset = Baner.objects.all()
            serializer = BanerSerializer(queryset, many=True)
            data = serializer.data
            cache.set(CACHE_KEY, data, timeout=CACHE_TIMEOUT)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Admin Permissions


class BanerDetailView(generics.RetrieveAPIView):
    serializer_class = BanerSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        baner_id = self.kwargs.get('pk')

        cache_key = f'baner_{baner_id}'
        baner = cache.get(cache_key)

        if not baner:
            queryset = Baner.objects.filter(pk=baner_id)
            baner = get_object_or_404(queryset, pk=baner_id)
            cache.set(cache_key, baner, timeout=60 * 15)

        return baner


class BanerUpdateView(generics.UpdateAPIView):
    queryset = Baner.objects.all()
    serializer_class = BanerSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        baner_id = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, pk=baner_id)



class BanerDeleteView(generics.DestroyAPIView):
    queryset = Baner.objects.all()
    serializer_class = BanerSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        baner_id = self.kwargs.get('pk')
        instance = get_object_or_404(self.queryset, pk=baner_id)
        self.perform_destroy(instance)
        return response.Response({"success": f"Банер id: {baner_id} успешно удалена!"}, status=status.HTTP_200_OK)
    















