from drf_yasg.utils import swagger_auto_schema
from ..serializers import *
from ..views import *




user_forget_password_send_description = """
Отправляет code на почту 

Необходимые поля:
{\n
    "email_or_phone":"user@gmail.com" -> type email
}
Приходит code в почту 
После получение code перейти по  user/forget-password/reset/



"""

user_forget_password_send_view = swagger_auto_schema(
    method='post',
    request_body=SendCodeSerializer,
    responses={200: SendCodeSerializer},
    operation_description=user_forget_password_send_description
)(ForgetPasswordSendCodeView.as_view())



user_forget_password_reset_description = """
Отправляет code на почту 

Необходимые поля:
{\n
    "code":"string", приходит 6 значный код Пример: MHG8F6
    "password":"string" type> str 8 значный
    "confirm_password":"string" type> str 8 значный для подтверждение
}

Пароль изменен!


"""

user_forget_password_reset_view = swagger_auto_schema(
    request_body=ForgetPasswordSerializer,
    responses={200: ForgetPasswordSerializer},
    operation_description=user_forget_password_reset_description
)(ForgetPasswordView.as_view())