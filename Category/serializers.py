from rest_framework import serializers
from .models import Category, PodCategory
import re
from django.utils.text import slugify
from transliterate import translit

class PodCategorySerializer(serializers.ModelSerializer):
    Category = Category()

    class Meta:
        model = PodCategory
        fields = ("id", "name", "category", "slug")
        read_only_fields = ("id", "slug")



class CategorySerializer(serializers.ModelSerializer):
    pod_categories = PodCategorySerializer(many=True, read_only=True,source='podcategory_set')
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "img", "pod_categories")
        read_only_fields = ("id", "slug")
    
    
    

    
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(translit(validated_data['name'], 'ru', reversed=True))
        return super().create(validated_data)
    
    def get_pod_categories(self, instance):
        pod_categories = instance.pod_categories.all()
        if pod_categories.exists():
            return PodCategorySerializer(pod_categories, many=True, context=self.context).data
        else:
            return []
        
    def to_representation(self, instance):
        data_category = super().to_representation(instance)
        data_category['pod_categories'] = self.get_pod_categories(instance)
        return data_category

