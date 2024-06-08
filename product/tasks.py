from .FCMmanage import sendPush
from .models import Recall
from rest_framework.response import Response
from rest_framework import status
from Shopx.celery import app



@app.task
def send_notification_discount(all_tokens,instance):
    result = sendPush(title=f'Скидка на {instance.name} цена {instance.discount}',
                        registration_token= all_tokens,
                        msg = "Большая скидка на продукт"
                        ,
                        )


@app.task
def send_push_notification_recall(title, whom):
    message = 'Отзыв'

    
    result = sendPush(title=title,
                    registration_token=whom.split(),
                    msg = message
                    ,
                    )
    return result