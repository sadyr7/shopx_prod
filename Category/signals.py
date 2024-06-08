from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category





@receiver(post_save, sender=Category)
def clear_cache_on_category_change(sender, instance, **kwargs):
    for query_params in ["", f"search={instance.name}"]:
        cache_key = f'category_list_{query_params}'
        cache.delete(cache_key)
    print("Cache cleared for category:", instance.name)



    
@receiver(post_delete, sender=Category)
def clear_cache_on_category_delete(sender, instance, **kwargs):
    # Удаление всех ключей кеша, содержащих категорию
    for query_params in ["", f"search={instance.name}"]:
        cache_key = f'category_list_{query_params}'
        cache.delete(cache_key)