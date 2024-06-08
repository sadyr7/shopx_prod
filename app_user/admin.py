from django.contrib import admin
from .models import User



class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['email_or_phone','id','is_active',"is_usual","username"]
    list_filter = ["is_active",'is_usual']
    search_fields = ["email_or_phone","is_seller"]

    

admin.site.register(User,UserProfileAdmin)