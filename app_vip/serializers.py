from rest_framework import serializers
from .models import Vip
from product.models import Product
from product. serializers import ProductSerializer


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']

class VipCreateSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=True)

    class Meta:
        model = Vip
        fields = ['id',"product",'icon']
    
        
        


class VipListSerializer(serializers.ModelSerializer):
    product = ProductSerializers()
    class Meta:
        model = Vip
        fields = ['id',"product",'icon']
        

    # def get_products(self, obj):
    #     products_queryset = obj.product.all()
    #     products_data = ProductSerializer(products_queryset, many=True).data
    #     return products_data
    