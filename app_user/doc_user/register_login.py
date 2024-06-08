from drf_yasg.utils import swagger_auto_schema
from ..serializers import *
from ..views import *


#========== User Register ================
user_register_description = """
Создает нового пользователя.

Необходимые поля:
{
    "email_or_phone": "user@gmail.com", -> type email # Email пользователя
    "username": "user", -> type str         # Имя пользователя
    "password": "string", должен содержать 8 чисел   # Пароль пользователя
    "password2": "string" должен содержать 8 чисел   # Подтверждение пароля
}

При успешной регистрации выводит:
201 - Код был отправлен на указанный реквизит
Проверяете почту приходит код и этот код отправляете в апи user/verification-register-code \n
там выдается выдается refresh и access токен 
"""

user_register_view = swagger_auto_schema(
    method='post',
    request_body=UserRegisterSerializer,
    responses={201: UserRegisterSerializer},
    operation_description=user_register_description
)(UserRegisterView.as_view())

#========== User Login ================

user_login_description = """
Создает нового пользователя.

Необходимые поля:
{
    "email_or_phone": "user@gmail.com",  # Email пользователя
    "password": "string",      # Пароль пользователя
}

При успешного входа  выводит:
200 - Код был отправлен на указанный реквизит


"""

user_login_view = swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: LoginSerializer},
    operation_description=user_login_description
)(UserLoginView.as_view())



