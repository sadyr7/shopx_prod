from rest_framework import mixins,generics,status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

from .models import SellerProfile
import random
import string
import requests


def generate_verification_code(length=6):
    """Generate a random verification code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))



def send_verification_code(email_or_phone):

    verification_code = generate_verification_code()

    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}\n\n'
    sender_email = 'kubanuch03@gmail.com'

    recipient_email = email_or_phone

    try:
        user_obj = SellerProfile.objects.get(email_or_phone=email_or_phone)
    except SellerProfile.DoesNotExist:
        user_obj = SellerProfile.objects.create(email_or_phone=email_or_phone)
    user_obj.code = verification_code
    user_obj.save()

    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)





def send_code_to_number(email_or_phone):
    login = 'erko'
    password = 'Bishkek2022'
    sender = 'SMSPRO.KG'

    transactionId = generate_verification_code()
    code = generate_verification_code()

    xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>
        <id>{transactionId}</id>
        <sender>{sender}</sender>
        <text>{code}</text>
        <phones>
            <phone>{email_or_phone}</phone>
        </phones>
    </message>"""


    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url, data=xml_data, headers=headers)
    user_obj = SellerProfile.objects.get(email_or_phone=email_or_phone)
    user_obj.code = code
    print(user_obj.number)
    user_obj.save()
    if response.status_code == 200:
        print('Ответ сервера:', response.text)



class CreateUserApiView(mixins.CreateModelMixin,generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем пользователя и получаем объект пользователя
        user = serializer.save()

        email_or_phone = serializer.validated_data.get('email_or_phone')

        if email_or_phone:
            if "@" in email_or_phone:
                serializer.validated_data['email'] = email_or_phone
                send_verification_code(email_or_phone=email_or_phone)
            else:
                serializer.validated_data['phone_number'] = email_or_phone
                send_code_to_number(email_or_phone=int(email_or_phone))

        return Response({"success": "Код был отправлен на указанный реквизит"}, status=status.HTTP_201_CREATED)



class CheckCode():
        @staticmethod
        def check_code(code):
            try:
                user = SellerProfile.objects.get(code=code)
                                
                user.is_active=True
                refresh = RefreshToken.for_user(user=user)
                user.auth_token_refresh = refresh
                user.auth_token_access = refresh.access_token
                user.save()

                return Response({
                    'detail': 'Successfully confirmed your code',
                    'is_seller':user.is_seller,
                    'id':user.id,
                    'email':user.email_or_phone,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'refresh_lifetime_days': refresh.lifetime.days,
                    'access_lifetime_days': refresh.access_token.lifetime.days
                })
            
            except:
                return Response({"error":"Пользователь не найден"})


class CodeChecking:

    def code_checking(self,request):
        # user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        new_password = serializer.validated_data.get('password')
        confirm_password = serializer.validated_data.get('confirm_password')


        check_code_result = CheckCode.check_code(code)
        if 'error' in check_code_result:
            return Response(check_code_result['error'], status=status.HTTP_400_BAD_REQUEST)
            
        if new_password != confirm_password:
            return Response({"success":"Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)
        
        



        user = SellerProfile.objects.get(code=code)
        # user.set_password(new_password)
        user.save()
        return {"success":"верный код"}
    








class ChangePassword:
    
    @staticmethod
    def change_password_on_profile(request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_new_password')

        if not check_password(old_password, user.password):
            print("old_password:", old_password)
            print("user.password:", user.password)
            return "Старый пароль неверный"
        
        if new_password != confirm_password:
            return "Пароли не совпадают"

        try:
            user.set_password(new_password)
            user.save()
            return "success"
        except Exception as e:
            return str(e)
    
    @staticmethod
    def compare_password(raw_password, hashed_password):
        """
        Функция для сравнения хешированного пароля с непосредственно введенным паролем.
        """
        return check_password(raw_password, hashed_password)
    
    
    def send_email_code(email_or_phone):

        try:
            SellerProfile.objects.get(email_or_phone=email_or_phone)
            if "@" in email_or_phone:
                send_verification_code(email_or_phone=email_or_phone)
                return Response({"success":"Код был отправлен на ваш email"})
            # elif "996" in email_or_phone:
            #     send_code_to_number(email_or_phone=int(email_or_phone))
            #     return Response({"success":"Код был отправлен на ваш номер"})
            else:
                return Response({"success":"The given data invalid"})
        except SellerProfile.DoesNotExist:
            return Response({"success":"Пользователь с таким емейлом не существует"})
        


    

