from rest_framework import serializers

from .models import Baner


class BanerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Baner
        fields = ['id','title','image',]
    