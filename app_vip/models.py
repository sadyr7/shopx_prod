from django.db import models
from product.models import Product
from django.utils import timezone
from django.core.cache import cache




class Vip(models.Model):
    icon = models.ImageField(upload_to='vip/', null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'vip_id: {self.id}'
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]

