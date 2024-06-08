from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response
from .models import Product
from .tasks import send_notification_discount
from datetime import datetime
from user_profiles.models import CustomUser

@receiver(post_save, sender=Product)
def notify_users_on_discount(sender, instance, created, **kwargs):
    title = f'Новая скидка для продукта {instance.name} {datetime.now()}'
    users_with_tokens = CustomUser.objects.exclude(device_token=None)

    if instance.discount is not None:
        send_notification_discount.delay(title, users_with_tokens)
        return Response('Отзыв был отправлен продавцу')
    