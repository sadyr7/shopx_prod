from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from app_user.models import User
from app_userseller.models import SellerProfile
from Category.models import Category, PodCategory
import re
from django.core.exceptions import ValidationError


class Size(models.Model):
    sizes = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.sizes
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            models.Index(fields=['sizes']),  
            
        ]

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL,null=True
    )
    podcategory = models.ForeignKey(
        PodCategory, related_name="pod_products", on_delete=models.CASCADE
    )
    user = models.ForeignKey(SellerProfile,related_name='products', on_delete=models.CASCADE,limit_choices_to={'is_seller': True})#
    name = models.CharField(max_length=200) #
    description = models.TextField(blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)#
    discount = models.PositiveIntegerField(blank=True, null=True)#  #delete
    discounted_price = models.PositiveBigIntegerField(blank=True,null=True)#
    size = models.ManyToManyField(Size)
    slug = models.SlugField(max_length=200)
    image1 = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True)#
    image2 = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True)
    image3 = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True)
    image4 = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)#
    updated = models.DateTimeField(auto_now=True)#

    # процент скидки
    # 
    #


    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["price"]),
            models.Index(fields=["-created"]),
        ]
    def clean(self):
        super().clean()
        if not self.name:
            raise ValidationError("Name cannot be empty")

        if not re.match("^[a-zA-Zа-яА-Я]", self.name, re.IGNORECASE):
            raise ValidationError("Name should start with a letter")

        if re.search("[^a-zA-Zа-яА-Я0-9\s]", self.name[1:], re.IGNORECASE):
            raise ValidationError("Name should not contain special characters or digits after the first character")

    def __str__(self):
        return self.name



class Recall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recall_images = models.ManyToManyField('RecallImages')
    def __str__(self):
        return f'{self.user} {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class RecallImages(models.Model):
    images = models.ImageField(upload_to='recall_image/%Y/%m/%d/',blank=True,null=True)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.product}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
