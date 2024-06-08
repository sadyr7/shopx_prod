from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recall', RecallViewSet, basename='recall')

urlpatterns = [

    path("product/list/", ProductListApiView.as_view(), name="product-list"),
    path('product/create/', ProductCreateApiView.as_view(), name='product-create'),
    path('viewed-products/<int:pk>/', ProductDetailView.as_view(), name='viewed-product-detail'),

    # path('update/product/<int:id>/', ProductUpdateApiView.as_view()),

    path('recall/list/<int:pk>/', RecallListApiView.as_view(), name='recall-list'),
    path('recall/image/create/', ReccallImageCreateApiView.as_view(), name='recall-image-create'),

    path("like/<int:pk>/", LikeView.as_view(), name="like"),

    path('', include(router.urls)),
    # path('viewed-products/', ViewedProductListCreate.as_view(), name='viewed-product-list'),

    path('size/list/', SizeListApiView.as_view(), name='list-create'),
    path('size/create/', SizeCreateApiView.as_view(), name='size-create'),
    path('size/detail/<int:pk>/', SizeDetailApiView.as_view(), name='size-create'),
    path('size/rud/<int:pk>/', SizeRUDApiView.as_view(), name='size-rud'),


]


