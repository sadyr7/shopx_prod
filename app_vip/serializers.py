from rest_framework import serializers
from .models import Vip
from product.models import Product, Recall
from django.db.models import Avg
from rest_framework import serializers




class RecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = ['rating', 'text']






class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discounted_price', 'rating']

    def get_rating(self, obj):
        recalls = Recall.objects.filter(product=obj)
        if recalls.exists():
            return recalls.aggregate(Avg('rating'))['rating__avg']
        return None
    


class VipCreateSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=True)

    class Meta:
        model = Vip
        fields = ['id',"product",'icon']
    
        
        


class VipListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Vip
        fields = ['id', 'product', 'icon']
        

    # def get_products(self, obj):
    #     products_queryset = obj.product.all()
    #     products_data = ProductSerializer(products_queryset, many=True).data
    #     return products_data
    