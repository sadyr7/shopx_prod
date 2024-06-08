from rest_framework.viewsets import generics
from rest_framework import response
from django.db import transaction
from django.core.cache import cache
from django.conf import settings
from .models import Vip
from .serializers import VipCreateSerializer, VipListSerializer




class VipListApiView(generics.ListAPIView):
    # queryset = Vip.objects.all()
    serializer_class = VipListSerializer

    def get_queryset(self):
        cache_key = 'vip_list'
        cache_ttl = getattr(settings, 'CACHE_TTL', 60)
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:  
            print(cached_queryset)
            return cached_queryset

        queryset = list(Vip.objects.prefetch_related('product').order_by('-id'))  
        cache.set(cache_key, queryset, timeout=cache_ttl)
        print('кеш не найден')
        return queryset


class VipDetailApiView(generics.RetrieveAPIView):
    queryset = Vip.objects.all()
    serializer_class = VipListSerializer


    # def retrieve(self, request, *args, **kwargs):
    #     vip_id = self.kwargs.get('pk')
    #     cache_key = 'vip_list'
        
    #     # Получаем кешированный список объектов Vip
    #     cached_vip_list = cache.get(cache_key)
    #     if cached_vip_list:
    #         # Поиск объекта Vip с заданным идентификатором
    #         cached_vip = next((vip for vip in cached_vip_list if vip['id'] == vip_id), None)
    #         if cached_vip:
    #             print(cached_vip)
    #             return response.Response(cached_vip)

    #     # Если объект не найден в кеше, получаем его из базы данных
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data

    #     # Кеширование объекта Vip
    #     if cached_vip_list is None:
    #         cached_vip_list = []
    #     cached_vip_list.append(data)
    #     cache.set(cache_key, cached_vip_list)

    #     print(' Нету детального в кеше ')
    #     return response.Response(data)
    
    def retrieve(self,request, *args, **kwargs):
        vip_id = self.kwargs.get('pk')
        cache_key = f'vip_list_{vip_id}'
        
        cached_vip = cache.get(cache_key)
        if cached_vip:
            print(cached_vip)
            return response.Response(cached_vip)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data)
        print(' нету детального в кеше ')
        return response.Response(data)
    



class VipCreateApiView(generics.CreateAPIView):
    queryset = Vip.objects.all()
    serializer_class = VipCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product') 
        
        
        if Vip.objects.select_related('product').filter(product__id=product_id).exists():
            return response.Response({"error": "this product already exists"})
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response({"success": f"Vip created successfully"})
    
    def perform_create(self, serializer):
        serializer.save()



class VipRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vip.objects.all()
    serializer_class = VipCreateSerializer