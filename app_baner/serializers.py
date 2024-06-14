from rest_framework import serializers

from .models import Baner


class BanerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    
    class Meta:
        model = Baner
        fields = ['id','title','image',]
    