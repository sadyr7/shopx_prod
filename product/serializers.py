from rest_framework import serializers
from .models import Product, Recall, RecallImages, Size
from app_user.serializers import  UserRecallSerializer
from app_vip.models import Vip
import re
from app_user.serializers import UserProfileSerializer, UserRecallSerializer

from app_userseller.models import SellerProfile


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id','sizes']
    
    def validate(self, attrs):
        sizes = attrs['sizes']

        if not re.match("[a-zA-Z]", sizes):
            raise serializers.ValidationError(
                'размер должен содержать только английские буквы'
            )

        attrs['sizes'] = sizes.upper()

        return attrs



class ProductDetailSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)
    discount = serializers.IntegerField(required=False)
    mid_ocenka = serializers.SerializerMethodField() 
    count_recall = serializers.SerializerMethodField() 
    icon_vip = serializers.SerializerMethodField() 

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'podcategory', 'user','size', 'name', 'slug', 'image1','image2','image3','image4', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated', 'likes', 'discount','mid_ocenka','count_recall','icon_vip'
        )
        read_only_fields = ('id', 'slug', 'created', 'updated','mid_ocenka',)

    def to_representation(self, instance):
        data_product = super().to_representation(instance)
        
        if instance.size is not None:
            data_product['size'] = SizeSerializer(instance.size.only('sizes'), many=True).data
        else:
            data_product['size'] = None
        
        return data_product
    
    
    def get_icon_vip(self, obj):
        if Vip.objects.filter(product=obj).exists():
            return Vip.objects.get(product=obj).icon.url
        else:
            return None

    def get_mid_ocenka(self, instance):
        recalls = instance.recall_set.all()
        if recalls.exists():
            total_rating = sum(recall.rating for recall in recalls)
            mid_ocenka = total_rating / recalls.count()
            return mid_ocenka
        else:
            return None

    def get_count_recall(self,instance):
        recalls = instance.recall_set.all()
        count_recall = recalls.count()
        return count_recall



class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)
    discount = serializers.IntegerField(required=False, allow_null=True)
    mid_ocenka = serializers.SerializerMethodField() 
    count_recall = serializers.SerializerMethodField() 
    discounted_price = serializers.IntegerField(required=False) 

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'podcategory', 'size', 'name', 'slug', 'image1', 'image2', 'image3', 'image4', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated', 'likes', 'discount', 'mid_ocenka', 'count_recall', 'discounted_price'
        )
        read_only_fields = ('id', 'slug', 'created', 'updated', 'mid_ocenka',)

    def apply_discount_to_price(self, price, discount):
        if discount > 0 and discount <= 100:
            discounted_price = price - (price * discount) // 100
            return discounted_price
        else:
            return price

    def create(self, validated_data):
        price = validated_data.get('price')
        discount = validated_data.get('discount', None)

        user = self.context['request'].user
        validated_data['user'] = user
        
        if price <= 0:
            raise serializers.ValidationError({"price": "Price must be a positive integer."})
        
        if discount is not None:
            if discount <= 0:
                raise serializers.ValidationError({"discount": "Discount must be a positive integer."})
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data['discounted_price'] = discounted_price
        else:
            validated_data['discounted_price'] = price 

        return super().create(validated_data)




    def get_mid_ocenka(self, instance):
        # Вычисляем среднюю оценку товара
        recalls = instance.recall_set.all()
        if recalls.exists():
            total_rating = sum(recall.rating for recall in recalls)
            mid_ocenka = total_rating / recalls.count()
            return mid_ocenka
        else:
            return None

    def get_count_recall(self,instance):
        recalls = instance.recall_set.all()
        count_recall = recalls.count()
        return count_recall


    
    


class RecallSerializer(serializers.ModelSerializer):
    user= UserRecallSerializer(read_only=True)
    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }

    def to_representation(self, instance):
        data_recall = super().to_representation(instance) 
        data_recall['user'] = UserRecallSerializer(instance.user.all(), many=True, context=self.context).data

        return data_recall


class RecallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecallImages
        fields = ['id','images']

