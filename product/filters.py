from django_filters import rest_framework as filters
from .models import Product

import django_filters

class CustomFilter(filters.FilterSet):
    created = filters.DateTimeFromToRangeFilter()
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ["category", "podcategory", "user", "price", "available", "created", ]
