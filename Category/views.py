from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Category, PodCategory
from .serializers import CategorySerializer, PodCategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import generics, response, status
from django.core.cache import cache
from django.conf import settings
import sys
from .castom_cache import save_category_to_cache







class CategoryCreateApiView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Дополнительная проверка на существование объекта с такими же данными
        name = serializer.validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            return response.Response({'error': 'Категория с таким именем уже существует'}, status=400)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        save_category_to_cache(serializer.instance)
        return response.Response(serializer.data, status=201, headers=headers)







class CategoryListView(ListAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        AllowAny,
    ]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]
 
    def get_queryset(self):
        cache_ttl = getattr(settings, 'CACHE_TTL',15*60)
        query_params = self.request.query_params.urlencode()
        cache_key = f'category_list_{query_params}'
        cached_queryset = cache.get(cache_key)
        memory = sys.getsizeof(cache_key)
        print(f"memory: {memory/1024}")
        if cached_queryset is not None:
            print('Возвращается из кеша')
            
            return cached_queryset
        
        query = self.request.query_params.get("search", "")
        queryset = Category.objects.filter(name__icontains=query)
        cache.set(cache_key, queryset, timeout=cache_ttl)
        print('Кеш не найден, сохранение в кеш')
        return queryset


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        AllowAny,   
    ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Создаем ключ кеша для данной категории
        cache_key = f'category_{instance.pk}'

        # Пытаемся получить данные из кеша
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            print('Данные категории возвращены из кеша')
            return response.Response(cached_data)

        # Если данных в кеше нет, сохраняем их и возвращаем
        cache.set(cache_key, data)
        print('Данные категории сохранены в кеш')
        return response.Response(data)

class PodCategoryViewSet(ModelViewSet):
    queryset = PodCategory.objects.all()
    serializer_class = PodCategorySerializer
    permission_classes = [
        AllowAny,
    ]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name", "category"]
    def get_queryset(self):
        query = self.request.query_params.get("search", "")
        return PodCategory.objects.filter(name__icontains=query)