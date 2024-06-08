from django.contrib import admin
from .models import Category, PodCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "img"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(PodCategory)
class PodCategory(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]