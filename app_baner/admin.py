from django.contrib import admin

from .models import Baner


class BanerAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    search_fields = ['title']


admin.site.register(Baner,BanerAdmin)
