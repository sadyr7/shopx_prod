from django.contrib import admin
from .models import SellerProfile
from app_user.models import User


class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['email_or_phone','is_seller','id']



    # def get_queryset(self, request):
    #     return SellerProfile.objects.filter(is_superuser=False)
admin.site.register(SellerProfile,SellerProfileAdmin)



