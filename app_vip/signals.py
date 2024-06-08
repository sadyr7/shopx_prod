from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from .models import Vip



@receiver(post_save, sender=Vip)
@receiver(post_delete, sender=Vip)
def clear_cache(sender, **kwargs):
    cache.delete('vip_list')
